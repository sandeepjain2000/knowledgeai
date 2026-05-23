"""
orchestrator.py — Ingestion orchestrator: parse → chunk → embed → store.
Handles retries, versioning, and upsert logic.
"""
import asyncio
import logging
import os
import shutil
from typing import Optional

from backend.config import UPLOADS_DIR, IMAGES_DIR
from backend.ingestion.parser import parse_file, extract_images
from backend.ingestion.chunker import chunk_text
from backend.ingestion.embedder import embed_texts
from backend.ingestion import metadata_db as db
from backend.retrieval.vector_store import upsert_chunks, delete_doc_vectors

logger = logging.getLogger(__name__)

# Async job queue (in-process, acts like SQS/Kafka for local use)
_job_queue: asyncio.Queue = asyncio.Queue()


async def enqueue(file_path: str, folder: str = "BRDs",
                  original_name: Optional[str] = None):
    """Add a file to the ingestion queue."""
    await _job_queue.put({
        "file_path": file_path,
        "folder": folder,
        "original_name": original_name or os.path.basename(file_path),
    })
    logger.info("Enqueued: %s", file_path)


async def worker():
    """Background worker that drains the job queue with retries."""
    logger.info("Ingestion worker started.")
    while True:
        job = await _job_queue.get()
        for attempt in range(3):
            try:
                await asyncio.to_thread(_ingest_file,
                                        job["file_path"],
                                        job["folder"],
                                        job["original_name"])
                break
            except Exception as e:
                logger.warning("Attempt %d failed for %s: %s",
                               attempt + 1, job["file_path"], e)
                if attempt == 2:
                    logger.error("Giving up on %s", job["file_path"])
                    db.log_ingestion(
                        doc_id="unknown",
                        file_name=job["original_name"],
                        status="failed",
                        error_msg=str(e),
                    )
                await asyncio.sleep(2 ** attempt)
        _job_queue.task_done()


def _ingest_file(file_path: str, folder: str, original_name: str):
    """Synchronous ingestion: parse → chunk → embed → store."""
    logger.info("Ingesting: %s", original_name)

    # 1. Parse
    text, meta = parse_file(file_path)
    if not text.strip():
        raise ValueError("Empty document after parsing")

    # Always use original_name (not the temp-file basename from the parser)
    file_name  = original_name
    file_type  = meta["file_type"]
    page_count = meta["page_count"]

    # 2. doc_id + hash — keyed on the real filename so re-uploads deduplicate correctly
    doc_id = db.make_doc_id(file_name)
    fhash  = db.file_hash(file_path)

    # Check if unchanged
    existing = db.get_document(doc_id)
    if existing and existing.get("file_hash") == fhash:
        logger.info("Unchanged file, skipping: %s", file_name)
        db.log_ingestion(doc_id, file_name, "skipped_unchanged")
        return

    # 3. Upsert document record → get version
    version_id = db.upsert_document(doc_id, file_name, file_type,
                                    folder, page_count, fhash)

    # 4. Soft-delete old chunks + old images from vector + keyword stores
    if existing:
        db.soft_delete_old_chunks(doc_id, version_id)
        delete_doc_vectors(doc_id, version_id - 1)
        # Remove old image records and files from disk
        old_filenames = db.delete_doc_images(doc_id)
        for fname in old_filenames:
            old_path = os.path.join(IMAGES_DIR, fname)
            try:
                if os.path.exists(old_path):
                    os.remove(old_path)
            except Exception:
                pass

    # 5. Chunk — pass page_word_offsets so each chunk is tagged with its page number
    page_word_offsets = meta.get("page_word_offsets")   # list of (page_num, start_word) or None
    chunks = chunk_text(text, doc_id, file_name, page_word_offsets=page_word_offsets)
    logger.info("  %d chunks created", len(chunks))

    # 6. Embed (batch)
    texts   = [c["text"] for c in chunks]
    vectors = embed_texts(texts)

    # 7. Store in vector DB + metadata DB + FTS
    upsert_chunks(chunks, vectors, version_id)
    for chunk in chunks:
        db.insert_chunk(
            chunk_id    = chunk["chunk_id"],
            doc_id      = chunk["doc_id"],
            file_name   = chunk["file_name"],
            chunk_index = chunk["chunk_index"],
            word_count  = chunk["word_count"],
            version_id  = version_id,
            body        = chunk["text"],
        )

    # 8. Copy to uploads dir for raw retrieval
    dest = os.path.join(UPLOADS_DIR, f"{doc_id}_{file_name}")
    if not os.path.exists(dest):
        shutil.copy2(file_path, dest)

    # 9. Extract images (screenshots) — best-effort, non-blocking
    try:
        images = extract_images(file_path, doc_id, IMAGES_DIR)
        for img in images:
            db.insert_doc_image(doc_id, file_name, img["page_num"], img["filename"])
        if images:
            logger.info("  %d image(s) extracted", len(images))
    except Exception as e:
        logger.warning("Image extraction skipped for %s: %s", file_name, e)

    db.log_ingestion(doc_id, file_name, "success")
    logger.info("Ingested: %s (v%d, %d chunks)", file_name, version_id, len(chunks))

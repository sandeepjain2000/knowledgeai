"""
vector_store.py — ChromaDB interface for storing and searching chunk embeddings.
"""
import os
import logging
from typing import List, Dict
import chromadb
from backend.config import CHROMA_DIR, TOP_K

# Disable telemetry without importing Settings (avoids pydantic v1 on Python 3.14)
os.environ.setdefault("ANONYMIZED_TELEMETRY", "false")
os.environ.setdefault("CHROMA_TELEMETRY", "false")

logger = logging.getLogger(__name__)

_client = None
_collection = None
COLLECTION_NAME = "knowledgeai_chunks"


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("ChromaDB collection ready: %s", COLLECTION_NAME)
    return _collection


def upsert_chunks(chunks: List[Dict], vectors: List[List[float]], version_id: int):
    """Store chunk vectors in ChromaDB."""
    col = _get_collection()
    ids        = [c["chunk_id"] for c in chunks]
    documents  = [c["text"] for c in chunks]
    metadatas  = [
        {
            "doc_id":      c["doc_id"],
            "file_name":   c["file_name"],
            "chunk_index": c["chunk_index"],
            "version_id":  version_id,
            "page_num":    c.get("page_num", 1),
        }
        for c in chunks
    ]
    col.upsert(ids=ids, embeddings=vectors, documents=documents, metadatas=metadatas)
    logger.debug("Upserted %d vectors", len(ids))


def delete_doc_vectors(doc_id: str, old_version: int):
    """Remove vectors belonging to old doc versions."""
    col = _get_collection()
    try:
        col.delete(where={"$and": [{"doc_id": {"$eq": doc_id}},
                                    {"version_id": {"$eq": old_version}}]})
    except Exception as e:
        logger.warning("Vector delete error (non-critical): %s", e)


def vector_search(query_vector: List[float], top_k: int = TOP_K) -> List[Dict]:
    """
    Return top_k results sorted by cosine similarity.
    Each result: {chunk_id, doc_id, file_name, chunk_index, text, score}
    """
    col = _get_collection()
    try:
        results = col.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, col.count() or 1),
            include=["documents", "metadatas", "distances"],
        )
    except Exception as e:
        logger.error("Vector search failed: %s", e)
        return []

    hits = []
    for i, chunk_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i]
        # ChromaDB cosine: distance = 1 - similarity
        similarity = 1.0 - distance
        meta = results["metadatas"][0][i]
        hits.append({
            "chunk_id":    chunk_id,
            "doc_id":      meta.get("doc_id", ""),
            "file_name":   meta.get("file_name", ""),
            "chunk_index": meta.get("chunk_index", 0),
            "page_num":    meta.get("page_num", 1),
            "text":        results["documents"][0][i],
            "vector_score": round(similarity, 4),
        })
    return hits


def collection_count() -> int:
    return _get_collection().count()

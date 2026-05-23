"""
metadata_db.py — SQLite database for document & chunk metadata + FTS5 keyword index.
"""
import sqlite3
import hashlib
import logging
import os
from datetime import datetime
from typing import List, Dict, Optional
from backend.config import SQLITE_PATH

logger = logging.getLogger(__name__)


def _conn() -> sqlite3.Connection:
    con = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    """Create all tables on first run."""
    with _conn() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS documents (
            doc_id       TEXT PRIMARY KEY,
            file_name    TEXT NOT NULL,
            file_type    TEXT,
            folder       TEXT DEFAULT 'BRDs',
            page_count   INTEGER DEFAULT 1,
            version_id   INTEGER DEFAULT 1,
            status       TEXT DEFAULT 'active',   -- active | deleted
            file_hash    TEXT,
            created_at   TEXT,
            updated_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id     TEXT PRIMARY KEY,
            doc_id       TEXT NOT NULL,
            file_name    TEXT NOT NULL,
            chunk_index  INTEGER,
            word_count   INTEGER,
            version_id   INTEGER DEFAULT 1,
            status       TEXT DEFAULT 'active',
            FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
            USING fts5(chunk_id, doc_id, file_name, body, tokenize='porter ascii');

        CREATE TABLE IF NOT EXISTS query_log (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text   TEXT,
            answer_len   INTEGER,
            source_count INTEGER,
            confidence   REAL,
            cache_hit    INTEGER DEFAULT 0,
            feedback     INTEGER DEFAULT 0,   -- 1 thumbs-up, -1 thumbs-down
            latency_ms   INTEGER,
            created_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS ingestion_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id      TEXT,
            file_name   TEXT,
            status      TEXT,
            error_msg   TEXT,
            created_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS qa_history (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            question     TEXT NOT NULL,
            answer       TEXT NOT NULL,
            sources      TEXT,          -- JSON list of source file names
            confidence   REAL,
            cache_hit    INTEGER DEFAULT 0,
            latency_ms   INTEGER,
            feedback     INTEGER DEFAULT 0,
            source_type  TEXT DEFAULT 'ui',   -- ui | excel | api
            is_faq       INTEGER DEFAULT 0,   -- promoted to FAQ?
            created_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS faqs (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            question     TEXT NOT NULL,
            answer       TEXT NOT NULL,
            sources      TEXT,
            confidence   REAL,
            created_at   TEXT,
            updated_at   TEXT
        );

        CREATE TABLE IF NOT EXISTS doc_images (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id         TEXT NOT NULL,
            file_name      TEXT NOT NULL,
            page_num       INTEGER,          -- NULL for DOCX (no reliable page layout)
            image_filename TEXT NOT NULL,
            created_at     TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_doc_images_doc ON doc_images(doc_id);
        """)
    logger.info("DB initialised at %s", SQLITE_PATH)


# ─── Documents ────────────────────────────────────────────────────────────────

def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def make_doc_id(file_name: str) -> str:
    return hashlib.md5(file_name.encode()).hexdigest()[:16]


def upsert_document(doc_id: str, file_name: str, file_type: str,
                    folder: str, page_count: int, fhash: str) -> int:
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        existing = con.execute(
            "SELECT version_id FROM documents WHERE doc_id=?", (doc_id,)
        ).fetchone()
        if existing:
            new_ver = existing["version_id"] + 1
            con.execute("""
                UPDATE documents SET file_name=?, file_type=?, folder=?,
                page_count=?, version_id=?, file_hash=?, updated_at=?, status='active'
                WHERE doc_id=?
            """, (file_name, file_type, folder, page_count, new_ver, fhash, now, doc_id))
            return new_ver
        else:
            con.execute("""
                INSERT INTO documents (doc_id, file_name, file_type, folder,
                page_count, version_id, file_hash, created_at, updated_at)
                VALUES (?,?,?,?,?,1,?,?,?)
            """, (doc_id, file_name, file_type, folder, page_count, fhash, now, now))
            return 1


def soft_delete_old_chunks(doc_id: str, current_version: int):
    with _conn() as con:
        con.execute("""
            UPDATE chunks SET status='deleted'
            WHERE doc_id=? AND version_id < ?
        """, (doc_id, current_version))


def insert_chunk(chunk_id: str, doc_id: str, file_name: str,
                 chunk_index: int, word_count: int, version_id: int, body: str):
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute("""
            INSERT OR REPLACE INTO chunks
            (chunk_id, doc_id, file_name, chunk_index, word_count, version_id, status)
            VALUES (?,?,?,?,?,?,'active')
        """, (chunk_id, doc_id, file_name, chunk_index, word_count, version_id))
        # FTS index
        con.execute("DELETE FROM chunks_fts WHERE chunk_id=?", (chunk_id,))
        con.execute("""
            INSERT INTO chunks_fts (chunk_id, doc_id, file_name, body)
            VALUES (?,?,?,?)
        """, (chunk_id, doc_id, file_name, body))


def get_document(doc_id: str) -> Optional[Dict]:
    with _conn() as con:
        row = con.execute(
            "SELECT * FROM documents WHERE doc_id=?", (doc_id,)
        ).fetchone()
    return dict(row) if row else None


def list_documents(folder: Optional[str] = None) -> List[Dict]:
    with _conn() as con:
        if folder:
            rows = con.execute(
                "SELECT * FROM documents WHERE status='active' AND folder=? ORDER BY updated_at DESC",
                (folder,)
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT * FROM documents WHERE status='active' ORDER BY updated_at DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def delete_document(doc_id: str):
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute(
            "UPDATE documents SET status='deleted', updated_at=? WHERE doc_id=?",
            (now, doc_id)
        )
        con.execute("UPDATE chunks SET status='deleted' WHERE doc_id=?", (doc_id,))


# ─── FTS Keyword Search ────────────────────────────────────────────────────────

def keyword_search(query: str, top_k: int = 10) -> List[Dict]:
    """BM25-style full-text search via SQLite FTS5."""
    with _conn() as con:
        # Escape FTS query
        safe_query = query.replace('"', '""')
        try:
            rows = con.execute("""
                SELECT f.chunk_id, f.doc_id, f.file_name,
                       bm25(chunks_fts) AS score
                FROM chunks_fts f
                JOIN chunks c ON c.chunk_id = f.chunk_id
                WHERE chunks_fts MATCH ? AND c.status='active'
                ORDER BY score
                LIMIT ?
            """, (safe_query, top_k)).fetchall()
        except Exception:
            # If FTS query fails (e.g. special chars), fall back to LIKE
            rows = con.execute("""
                SELECT f.chunk_id, f.doc_id, f.file_name,
                       -1.0 AS score
                FROM chunks_fts f
                JOIN chunks c ON c.chunk_id = f.chunk_id
                WHERE f.body LIKE ? AND c.status='active'
                LIMIT ?
            """, (f"%{query}%", top_k)).fetchall()
    return [dict(r) for r in rows]


# ─── Query + Feedback logging ──────────────────────────────────────────────────

def log_query(query_text: str, answer_len: int, source_count: int,
              confidence: float, cache_hit: bool, latency_ms: int):
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute("""
            INSERT INTO query_log
            (query_text, answer_len, source_count, confidence, cache_hit, latency_ms, created_at)
            VALUES (?,?,?,?,?,?,?)
        """, (query_text, answer_len, source_count, confidence,
              int(cache_hit), latency_ms, now))


def record_feedback(query_id: int, vote: int):
    with _conn() as con:
        con.execute(
            "UPDATE query_log SET feedback=? WHERE id=?", (vote, query_id)
        )


def get_analytics() -> Dict:
    with _conn() as con:
        total_docs  = con.execute("SELECT COUNT(*) FROM documents WHERE status='active'").fetchone()[0]
        total_chunks = con.execute("SELECT COUNT(*) FROM chunks WHERE status='active'").fetchone()[0]
        total_queries = con.execute("SELECT COUNT(*) FROM query_log").fetchone()[0]
        cache_hits   = con.execute("SELECT COUNT(*) FROM query_log WHERE cache_hit=1").fetchone()[0]
        avg_conf     = con.execute("SELECT AVG(confidence) FROM query_log").fetchone()[0] or 0
        avg_lat      = con.execute("SELECT AVG(latency_ms) FROM query_log").fetchone()[0] or 0
        top_queries  = con.execute("""
            SELECT query_text, COUNT(*) as cnt
            FROM query_log GROUP BY query_text
            ORDER BY cnt DESC LIMIT 10
        """).fetchall()
        recent_ingestions = con.execute("""
            SELECT * FROM ingestion_log ORDER BY created_at DESC LIMIT 20
        """).fetchall()
    return {
        "total_docs": total_docs,
        "total_chunks": total_chunks,
        "total_queries": total_queries,
        "cache_hit_rate": round(cache_hits / max(1, total_queries), 3),
        "avg_confidence": round(avg_conf, 3),
        "avg_latency_ms": round(avg_lat),
        "top_queries": [dict(r) for r in top_queries],
        "recent_ingestions": [dict(r) for r in recent_ingestions],
    }


def log_ingestion(doc_id: str, file_name: str, status: str, error_msg: str = ""):
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute("""
            INSERT INTO ingestion_log (doc_id, file_name, status, error_msg, created_at)
            VALUES (?,?,?,?,?)
        """, (doc_id, file_name, status, error_msg, now))


# ─── Q&A History ──────────────────────────────────────────────────────────────

def save_history(question: str, answer: str, sources: List[str],
                 confidence: float, cache_hit: bool, latency_ms: int,
                 source_type: str = "ui") -> int:
    """Save a Q&A pair. Returns the new row id."""
    import json
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        cur = con.execute("""
            INSERT INTO qa_history
            (question, answer, sources, confidence, cache_hit, latency_ms, source_type, created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (question, answer, json.dumps(sources), confidence,
              int(cache_hit), latency_ms, source_type, now))
        return cur.lastrowid


def get_history(limit: int = 100, offset: int = 0,
                source_type: Optional[str] = None) -> List[Dict]:
    import json
    with _conn() as con:
        if source_type:
            rows = con.execute("""
                SELECT * FROM qa_history WHERE source_type=?
                ORDER BY created_at DESC LIMIT ? OFFSET ?
            """, (source_type, limit, offset)).fetchall()
        else:
            rows = con.execute("""
                SELECT * FROM qa_history
                ORDER BY created_at DESC LIMIT ? OFFSET ?
            """, (limit, offset)).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["sources"] = json.loads(d["sources"] or "[]")
        except Exception:
            d["sources"] = []
        result.append(d)
    return result


def update_history_feedback(history_id: int, vote: int):
    with _conn() as con:
        con.execute("UPDATE qa_history SET feedback=? WHERE id=?", (vote, history_id))


# ─── FAQ Management ───────────────────────────────────────────────────────────

def promote_to_faq(history_id: int) -> int:
    """Promote a history entry to the FAQ table. Returns faq id."""
    import json
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        row = con.execute(
            "SELECT * FROM qa_history WHERE id=?", (history_id,)
        ).fetchone()
        if not row:
            raise ValueError(f"History id {history_id} not found")
        row = dict(row)
        cur = con.execute("""
            INSERT INTO faqs (question, answer, sources, confidence, created_at, updated_at)
            VALUES (?,?,?,?,?,?)
        """, (row["question"], row["answer"], row["sources"],
              row["confidence"], now, now))
        faq_id = cur.lastrowid
        con.execute("UPDATE qa_history SET is_faq=1 WHERE id=?", (history_id,))
    return faq_id


def get_faqs() -> List[Dict]:
    import json
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM faqs ORDER BY created_at DESC"
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["sources"] = json.loads(d["sources"] or "[]")
        except Exception:
            d["sources"] = []
        result.append(d)
    return result


def delete_faq(faq_id: int):
    with _conn() as con:
        con.execute("DELETE FROM faqs WHERE id=?", (faq_id,))


def update_faq(faq_id: int, answer: str):
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute(
            "UPDATE faqs SET answer=?, updated_at=? WHERE id=?",
            (answer, now, faq_id)
        )


# ─── Document Images ──────────────────────────────────────────────────────────

def insert_doc_image(doc_id: str, file_name: str, page_num, image_filename: str):
    """Record an extracted image file linked to a document page."""
    now = datetime.utcnow().isoformat()
    with _conn() as con:
        con.execute("""
            INSERT INTO doc_images (doc_id, file_name, page_num, image_filename, created_at)
            VALUES (?,?,?,?,?)
        """, (doc_id, file_name, page_num, image_filename, now))


def delete_doc_images(doc_id: str) -> List[str]:
    """Remove all image records for a doc. Returns list of image filenames to delete from disk."""
    with _conn() as con:
        rows = con.execute(
            "SELECT image_filename FROM doc_images WHERE doc_id=?", (doc_id,)
        ).fetchall()
        filenames = [r["image_filename"] for r in rows]
        con.execute("DELETE FROM doc_images WHERE doc_id=?", (doc_id,))
    return filenames


def get_images_for_doc(doc_id: str) -> List[Dict]:
    """All images for a document, ordered by page."""
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM doc_images WHERE doc_id=? ORDER BY page_num NULLS LAST",
            (doc_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_images_for_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Given a list of retrieved chunk dicts (each with doc_id + page_num),
    return matching images. For DOCX docs (page_num=None), return all doc images.
    Deduplicates by image_filename.
    """
    seen = set()
    results = []
    with _conn() as con:
        for chunk in chunks:
            doc_id   = chunk.get("doc_id", "")
            page_num = chunk.get("page_num")   # may be None for DOCX

            if page_num is not None:
                # PDF: fetch images for this page ± 1 (catches split layouts)
                pages = [max(1, page_num - 1), page_num, page_num + 1]
                placeholders = ",".join("?" * len(pages))
                rows = con.execute(
                    f"SELECT * FROM doc_images WHERE doc_id=? AND page_num IN ({placeholders})",
                    (doc_id, *pages)
                ).fetchall()
            else:
                # DOCX: no page info — return all images for the document
                rows = con.execute(
                    "SELECT * FROM doc_images WHERE doc_id=?", (doc_id,)
                ).fetchall()

            for r in rows:
                key = r["image_filename"]
                if key not in seen:
                    seen.add(key)
                    results.append(dict(r))

    return results


def faq_lookup(question: str) -> Optional[Dict]:
    """Exact or close match lookup in the FAQ table."""
    import json
    q_lower = question.strip().lower()
    with _conn() as con:
        rows = con.execute("SELECT * FROM faqs").fetchall()
    for r in rows:
        d = dict(r)
        if d["question"].strip().lower() == q_lower:
            try:
                d["sources"] = json.loads(d["sources"] or "[]")
            except Exception:
                d["sources"] = []
            return d
    return None

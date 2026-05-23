"""
hybrid_search.py — Combine vector search + BM25 keyword search with RRF fusion.
"""
import logging
from typing import List, Dict
from backend.config import TOP_K
from backend.retrieval.vector_store import vector_search
from backend.ingestion.metadata_db import keyword_search

logger = logging.getLogger(__name__)

RRF_K = 60  # Reciprocal Rank Fusion constant


def hybrid_search(query_vector: List[float], query_text: str,
                  top_k: int = TOP_K) -> List[Dict]:
    """
    Fuse vector search and BM25 keyword search using Reciprocal Rank Fusion.
    Returns merged list of hits with a combined_score.
    """
    # 1. Vector search
    vec_hits = vector_search(query_vector, top_k=top_k)

    # 2. Keyword search
    kw_hits  = keyword_search(query_text, top_k=top_k)

    # Build chunk_id → result maps
    vec_map = {h["chunk_id"]: h for h in vec_hits}
    kw_map  = {h["chunk_id"]: h for h in kw_hits}

    all_ids = list({*vec_map.keys(), *kw_map.keys()})

    # 3. RRF scoring
    vec_rank = {h["chunk_id"]: rank for rank, h in enumerate(vec_hits, 1)}
    kw_rank  = {h["chunk_id"]: rank for rank, h in enumerate(kw_hits, 1)}

    scored = []
    for cid in all_ids:
        rrf = 0.0
        if cid in vec_rank:
            rrf += 1.0 / (RRF_K + vec_rank[cid])
        if cid in kw_rank:
            rrf += 1.0 / (RRF_K + kw_rank[cid])

        # Merge metadata: prefer vector hit (has full text)
        hit = vec_map.get(cid) or {}
        if not hit:
            kw = kw_map[cid]
            hit = {
                "chunk_id":    cid,
                "doc_id":      kw.get("doc_id", ""),
                "file_name":   kw.get("file_name", ""),
                "chunk_index": 0,
                "text":        "",
                "vector_score": 0.0,
            }

        hit["combined_score"] = round(rrf, 6)
        scored.append(hit)

    scored.sort(key=lambda x: x["combined_score"], reverse=True)
    return scored[:top_k]

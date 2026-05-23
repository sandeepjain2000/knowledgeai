"""
reranker.py — Re-rank candidate chunks and compute a confidence score.

All intermediate scores are normalised to [0, 1] before blending so the
final rerank_score is also in [0, 1].  This value is displayed directly as a
percentage in the UI (e.g. 0.82 → 82 %).
"""
import math
import logging
from typing import List, Dict, Tuple
from backend.config import RERANK_TOP_N, CONFIDENCE_THRESHOLD

logger = logging.getLogger(__name__)

# Maximum possible RRF score when a chunk ranks #1 in both vector AND keyword
# lists with the default RRF_K = 60:  2 / (60 + 1) ≈ 0.0328
_RRF_K   = 60
_MAX_RRF = 2.0 / (_RRF_K + 1)          # ≈ 0.0328 — used for normalisation


def _token_overlap_score(query: str, passage: str) -> float:
    """
    Recall-oriented token overlap: fraction of query tokens found in passage.
    Returns a value in [0, 1].
    """
    q_tokens = set(query.lower().split())
    p_tokens  = set(passage.lower().split())
    if not q_tokens:
        return 0.0
    matched = q_tokens & p_tokens
    return len(matched) / len(q_tokens)


def rerank(query: str, hits: List[Dict]) -> Tuple[List[Dict], float]:
    """
    Re-rank hits and return (top_n_hits, confidence ∈ [0, 1]).

    Scoring blend (all components in [0, 1]):
      50 % vector cosine similarity
      40 % normalised hybrid-RRF score
      10 % token overlap (recall)
    """
    for hit in hits:
        vec_sc   = float(hit.get("vector_score", 0.0))           # already 0-1
        rrf_raw  = float(hit.get("combined_score", 0.0))         # tiny (≤ 0.033)
        rrf_norm = min(rrf_raw / _MAX_RRF, 1.0) if rrf_raw > 0 else 0.0
        overlap  = _token_overlap_score(query, hit.get("text", ""))

        hit["rerank_score"] = round(
            0.50 * vec_sc +
            0.40 * rrf_norm +
            0.10 * overlap,
            4,
        )

    hits.sort(key=lambda x: x["rerank_score"], reverse=True)
    top = hits[:RERANK_TOP_N]

    # Confidence = mean rerank_score of top-N results (already 0-1)
    if top:
        confidence = round(sum(h["rerank_score"] for h in top) / len(top), 3)
    else:
        confidence = 0.0

    return top, confidence


def is_confident(confidence: float) -> bool:
    return confidence >= CONFIDENCE_THRESHOLD

"""
formatter.py — Attach citations and format the final answer for the UI.
"""
from typing import List, Dict


def format_response(answer: str, chunks: List[Dict],
                    confidence: float, cache_hit: bool) -> Dict:
    """
    Build the structured response payload sent to the frontend.
    """
    # Build unique source list
    seen = set()
    sources = []
    for chunk in chunks:
        key = (chunk["file_name"], chunk.get("chunk_index", 0))
        if key not in seen:
            seen.add(key)
            sources.append({
                "file_name":   chunk["file_name"],
                "doc_id":      chunk.get("doc_id", ""),
                "chunk_index": chunk.get("chunk_index", 0),
                "score":       round(chunk.get("rerank_score", chunk.get("vector_score", 0)), 3),
            })

    sources.sort(key=lambda s: s["score"], reverse=True)

    return {
        "answer":     answer,
        "sources":    sources,
        "confidence": confidence,
        "cache_hit":  cache_hit,
        "follow_ups": _suggest_follow_ups(answer),
    }


def _suggest_follow_ups(answer: str) -> List[str]:
    """Generate 3 simple follow-up question starters based on answer length."""
    if len(answer) < 50:
        return []
    return [
        "Can you elaborate on this in more detail?",
        "What are the key risks or constraints mentioned?",
        "How does this compare to industry best practices?",
    ]

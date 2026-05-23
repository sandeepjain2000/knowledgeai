"""
embedder.py — Generate embeddings via OpenAI API (text-embedding-3-small).
"""
import logging
from typing import List
from openai import OpenAI
from backend.config import OPENAI_API_KEY, EMBEDDING_MODEL

logger = logging.getLogger(__name__)
_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def embed_texts(texts: List[str], batch_size: int = 100) -> List[List[float]]:
    """
    Embed a list of texts, batching to stay within API limits.
    Returns list of 1536-dim float vectors.
    """
    client = _get_client()
    all_vectors = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i: i + batch_size]
        # Clean: replace newlines (OpenAI recommendation)
        batch = [t.replace("\n", " ") for t in batch]
        try:
            response = client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch,
            )
            vectors = [item.embedding for item in response.data]
            all_vectors.extend(vectors)
        except Exception as e:
            logger.error(f"Embedding error on batch {i}: {e}")
            raise

    return all_vectors


def embed_single(text: str) -> List[float]:
    """Embed a single string and return its vector."""
    return embed_texts([text])[0]

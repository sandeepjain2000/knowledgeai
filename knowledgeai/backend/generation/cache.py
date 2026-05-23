"""
cache.py — In-memory semantic cache.
Stores (query_vector, response) pairs; on new query, checks cosine similarity.
If similarity > threshold, returns cached answer without hitting the LLM.
"""
import math
import logging
from collections import OrderedDict
from typing import Optional, Dict, Any, List
from backend.config import CACHE_MAX_SIZE, CACHE_SIM_THRESHOLD

logger = logging.getLogger(__name__)


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na  = math.sqrt(sum(x * x for x in a))
    nb  = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class SemanticCache:
    def __init__(self, max_size: int = CACHE_MAX_SIZE,
                 sim_threshold: float = CACHE_SIM_THRESHOLD):
        self._store: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.max_size    = max_size
        self.sim_threshold = sim_threshold
        self.hits = 0
        self.misses = 0

    def lookup(self, query_vector: List[float],
               model: str = "") -> Optional[Dict]:
        """Return cached entry if a similar query exists for the same model."""
        best_score = 0.0
        best_entry = None
        for key, entry in self._store.items():
            # Only match entries from the same model
            if entry.get("model", "") != model:
                continue
            score = _cosine(query_vector, entry["vector"])
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_score >= self.sim_threshold and best_entry:
            self.hits += 1
            logger.debug("Cache HIT (sim=%.3f, model=%s)", best_score, model)
            self._store.move_to_end(best_entry["key"])
            return best_entry["payload"]

        self.misses += 1
        return None

    def store(self, query_text: str, query_vector: List[float],
              payload: Dict, model: str = ""):
        """Add a new entry; evict oldest if at capacity."""
        if len(self._store) >= self.max_size:
            self._store.popitem(last=False)

        # Include model in key so same query with different models coexist
        key = f"{model}::{query_text[:120]}"
        self._store[key] = {
            "key":     key,
            "model":   model,
            "vector":  query_vector,
            "payload": payload,
        }
        self._store.move_to_end(key)

    @property
    def stats(self) -> Dict:
        total = self.hits + self.misses
        return {
            "size":      len(self._store),
            "hits":      self.hits,
            "misses":    self.misses,
            "hit_rate":  round(self.hits / max(1, total), 3),
        }


# Singleton
_cache = SemanticCache()


def cache_lookup(query_vector: List[float],
                 model: str = "") -> Optional[Dict]:
    return _cache.lookup(query_vector, model=model)


def cache_store(query_text: str, query_vector: List[float],
                payload: Dict, model: str = ""):
    _cache.store(query_text, query_vector, payload, model=model)


def cache_stats() -> Dict:
    return _cache.stats

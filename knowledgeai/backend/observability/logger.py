"""
logger.py — Centralised logging configuration + observability helpers.
"""
import logging
import sys
import time
from contextlib import contextmanager
from typing import Dict


def setup_logging(level: str = "INFO"):
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Silence noisy third-party libs
    for lib in ("httpx", "httpcore", "chromadb", "openai"):
        logging.getLogger(lib).setLevel(logging.WARNING)


@contextmanager
def timer(label: str = "operation"):
    """Context manager that returns elapsed milliseconds."""
    start = time.perf_counter()
    result = {}
    try:
        yield result
    finally:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        result["ms"] = elapsed_ms
        logging.getLogger(__name__).debug("%s took %d ms", label, elapsed_ms)


class QueryMetrics:
    """Collect per-request metrics for observability."""
    def __init__(self):
        self.start = time.perf_counter()
        self.stages: Dict[str, int] = {}

    def mark(self, stage: str):
        elapsed = int((time.perf_counter() - self.start) * 1000)
        self.stages[stage] = elapsed

    @property
    def total_ms(self) -> int:
        return int((time.perf_counter() - self.start) * 1000)

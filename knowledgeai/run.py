"""
run.py — Start KnowledgeAI server.
The file watcher and BRDs folder scan are started inside FastAPI's startup event,
so they share the same asyncio event loop as uvicorn.
Usage:  python run.py
"""
import uvicorn
from backend.config import HOST, PORT
from backend.observability.logger import setup_logging

setup_logging()

if __name__ == "__main__":
    print("""
  ╔══════════════════════════════════════╗
  ║   KnowledgeAI — BRD RAG Platform    ║
  ╚══════════════════════════════════════╝
  """)
    print(f"  → Opening at http://localhost:{PORT}\n")
    uvicorn.run(
        "backend.main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info",
    )

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL           = os.getenv("LLM_MODEL", "gpt-4o")
EMBEDDING_MODEL     = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Gemini
GEMINI_API_KEY      = os.getenv("GEMINI_API_KEY", "")

# Anthropic
ANTHROPIC_API_KEY   = os.getenv("ANTHROPIC_API_KEY", "")

# Paths
BASE_DIR            = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRD_FOLDER          = os.getenv("BRD_FOLDER", os.path.join(BASE_DIR, "BRDs"))
DATA_DIR            = os.path.join(BASE_DIR, "data")
CHROMA_DIR          = os.path.join(DATA_DIR, "chroma")
SQLITE_PATH         = os.path.join(DATA_DIR, "metadata.db")
UPLOADS_DIR         = os.path.join(DATA_DIR, "uploads")
IMAGES_DIR          = os.path.join(DATA_DIR, "images")
EXCEL_OUTPUT_DIR    = os.getenv("EXCEL_OUTPUT_DIR", os.path.join(BASE_DIR, "BRDs"))

# Server
HOST                = os.getenv("HOST", "0.0.0.0")
PORT                = int(os.getenv("PORT", 8000))

# Chunking — larger chunks preserve more context per passage
CHUNK_SIZE          = int(os.getenv("CHUNK_SIZE", 600))       # words (up from 400)
CHUNK_OVERLAP       = int(os.getenv("CHUNK_OVERLAP", 80))     # words (up from 50)

# Retrieval — cast wider net, pass more context to LLM
TOP_K               = int(os.getenv("TOP_K", 25))             # up from 10
RERANK_TOP_N        = int(os.getenv("RERANK_TOP_N", 6))       # up from 3
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.08))  # down from 0.20

# Semantic cache
CACHE_MAX_SIZE      = int(os.getenv("CACHE_MAX_SIZE", 500))
CACHE_SIM_THRESHOLD = float(os.getenv("CACHE_SIMILARITY_THRESHOLD", 0.92))

# Q&A History & FAQ
HISTORY_ENABLED     = os.getenv("HISTORY_ENABLED", "true").lower() == "true"

# Ensure dirs exist
for d in [DATA_DIR, CHROMA_DIR, UPLOADS_DIR, IMAGES_DIR, BRD_FOLDER, EXCEL_OUTPUT_DIR]:
    os.makedirs(d, exist_ok=True)

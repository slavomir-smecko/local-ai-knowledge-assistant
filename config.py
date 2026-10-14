
import os
from pathlib import Path

from dotenv import load_dotenv


# Project paths

BASE_DIR = Path(__file__).resolve().parent

# Load .env for local Python commands.
# Existing environment variables take precedence.
load_dotenv(BASE_DIR / ".env")

VECTOR_DB_PATH = BASE_DIR / "vector_db" / "chroma"
DOCUMENTS_PATH = BASE_DIR / "documents"


# Vector database

COLLECTION_NAME = "rag_documents"


# Embeddings

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2",
)


# LLM

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gemma3:4b",
)


# Retrieval

SEARCH_K = int(os.getenv("SEARCH_K", "20"))
TOP_K = int(os.getenv("TOP_K", "5"))
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "1.15"))


# Chunking

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

"""
Centralized configuration for the Jarvis application.
Reads all settings from environment variables with sensible defaults.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the app directory
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


@dataclass(slots=True)
class LlmConfig:
    """Configuration for the Ollama LLM client."""
    model: str = field(default_factory=lambda: os.getenv("OLLAMA_MODEL", "tinyllama:latest"))
    temp: float = field(default_factory=lambda: float(os.getenv("OLLAMA_TEMPERATURE", "0.7")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("OLLAMA_MAX_RETRIES", "3")))
    timeout: float = field(default_factory=lambda: float(os.getenv("OLLAMA_TIMEOUT", "30")))


@dataclass(slots=True)
class DatabaseConfig:
    """Configuration for the PostgreSQL database."""
    url: str = field(default_factory=lambda: os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:admin@localhost:5432/agentdb"
    ))
    pool_size: int = field(default_factory=lambda: int(os.getenv("DB_POOL_SIZE", "20")))
    max_overflow: int = field(default_factory=lambda: int(os.getenv("DB_MAX_OVERFLOW", "10")))
    pool_recycle: int = field(default_factory=lambda: int(os.getenv("DB_POOL_RECYCLE", "3600")))
    echo: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")


@dataclass(slots=True)
class QdrantConfig:
    """Configuration for the Qdrant vector database."""
    host: str = field(default_factory=lambda: os.getenv("QDRANT_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.getenv("QDRANT_PORT", "6333")))
    collection: str = field(default_factory=lambda: os.getenv("QDRANT_COLLECTION", "agent_memory"))
    api_key: str = field(default_factory=lambda: os.getenv("QDRANT_API_KEY", ""))


@dataclass(slots=True)
class EmbeddingConfig:
    """Configuration for the HuggingFace embedding model."""
    model_name: str = field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en"))


@dataclass(slots=True)
class MemoryConfig:
    """Configuration for the memory / RAG system."""
    top_k: int = field(default_factory=lambda: int(os.getenv("MEMORY_TOP_K", "3")))
    similarity_threshold: float = field(
        default_factory=lambda: float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.7"))
    )


# ── Singleton instances ────────────────────────────────────────────
llm_config = LlmConfig()
db_config = DatabaseConfig()
qdrant_config = QdrantConfig()
embedding_config = EmbeddingConfig()
memory_config = MemoryConfig()

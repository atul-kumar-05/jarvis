"""
Qdrant vector store initialization.
Reads connection details from centralized config.
"""

from typing import Optional

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from app.core.config import embedding_config, qdrant_config
from app.core.logging import logger

# ── Qdrant client ──────────────────────────────────────────────────
client = QdrantClient(host=qdrant_config.host, port=qdrant_config.port)

# ── Embedding model ────────────────────────────────────────────────
embed_model = HuggingFaceEmbedding(model_name=embedding_config.model_name)

# ── Vector store ───────────────────────────────────────────────────
try:
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=qdrant_config.collection,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
except Exception as exc:
    logger.warning("Qdrant not available at startup: %s", exc)
    vector_store = None
    storage_context = None

# ── Lazy index singleton ──────────────────────────────────────────
_index: Optional[VectorStoreIndex] = None


def get_index() -> Optional[VectorStoreIndex]:
    """Get or create the vector store index. Returns ``None`` if Qdrant is unavailable."""
    global _index

    if vector_store is None:
        logger.warning("Vector store not initialised — Qdrant may be offline")
        return None

    if _index is None:
        try:
            _index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
                embed_model=embed_model,
            )
            logger.info("Vector store index created successfully")
        except Exception as exc:
            logger.error("Failed to initialise vector index: %s", exc)
            return None

    return _index
"""
LLaMA Index global settings — configures the LLM and embedding model.
Reads model names from environment via centralized config.
"""

from app.config.settings import embedding_config, llm_config
from app.core.logging import logger

try:
    from llama_index.core import Settings
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.ollama import Ollama

    Settings.llm = Ollama(
        model=llm_config.model.replace(":latest", ""),
        request_timeout=llm_config.timeout,
    )

    Settings.embed_model = HuggingFaceEmbedding(
        model_name=embedding_config.model_name,
    )

    logger.info(
        "LLaMA Index configured | LLM=%s | Embedding=%s",
        llm_config.model,
        embedding_config.model_name,
    )
except Exception as exc:
    logger.warning("LLaMA Index setup failed (non-fatal): %s", exc)

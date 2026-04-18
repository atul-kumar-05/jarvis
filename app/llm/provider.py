"""
LLM provider — single source of truth for the LLM singleton.
"""

from app.core.config import LlmConfig
from app.llm.llm_client import LlmClient
from app.llm.llm_service import LlmService

# Singleton setup
_config = LlmConfig()
_client = LlmClient(_config)
llm_service = LlmService(_client)
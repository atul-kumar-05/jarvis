"""LLM provider — single source of truth for the LLM singleton."""

from app.config.settings import LlmConfig
from app.llm.client import LlmClient
from app.llm.service import LlmService

_config = LlmConfig()
_client = LlmClient(_config)
llm_service = LlmService(_client)
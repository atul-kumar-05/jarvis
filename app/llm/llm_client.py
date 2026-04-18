"""
LLM client — thin wrapper around ChatOllama with latency logging.
"""

import time
from typing import Optional

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from app.core.config import LlmConfig
from app.core.logging import logger


class LlmClient:
    """Low-level LLM client. Use ``LlmService`` for retry-aware calls."""

    def __init__(self, config: LlmConfig) -> None:
        self.config = config
        self.chat_ollama = ChatOllama(
            model=config.model,
            temperature=config.temp,
        )

    def invoke(self, prompt: str) -> str:
        """Send a single prompt to the LLM and return the text response."""
        start_time = time.time()

        response = self.chat_ollama.invoke([HumanMessage(content=prompt)])

        duration = time.time() - start_time
        logger.info(
            "LLM call completed | model=%s | latency=%.3fs",
            self.config.model,
            duration,
        )

        return response.content

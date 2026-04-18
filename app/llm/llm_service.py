"""
LLM service — adds retry logic with exponential backoff on top of LlmClient.
"""

import time

from app.core.logging import logger
from app.llm.llm_client import LlmClient
from app.llm.llm_exception import LLMError


class LlmService:
    """High-level LLM interface with automatic retries."""

    def __init__(self, llm: LlmClient) -> None:
        self.client = llm

    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt, retrying on transient failures.

        Raises:
            LLMError: If all retry attempts are exhausted.
        """
        last_exception: Exception | None = None
        max_retries = self.client.config.max_retries

        for attempt in range(1, max_retries + 1):
            try:
                return self.client.invoke(prompt)
            except Exception as exc:
                last_exception = exc
                logger.warning(
                    "LLM retry attempt %d/%d failed: %s",
                    attempt,
                    max_retries,
                    exc,
                )
                time.sleep(2 ** (attempt - 1))

        detail = str(last_exception) if last_exception else "unknown error"
        raise LLMError(
            f"LLM generation failed after {max_retries} retries: {detail}"
        ) from last_exception

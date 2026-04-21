"""Custom exceptions for the LLM subsystem."""


class LLMError(Exception):
    """Raised when the LLM fails after all retry attempts."""
    pass

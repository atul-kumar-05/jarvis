"""
LLM package — exposes a single ``generate()`` function.

Uses the singleton from ``provider.py`` (no duplicate setup).
"""

from app.llm.provider import llm_service


def generate(prompt: str) -> str:
    """Generate text from a prompt using the configured LLM."""
    return llm_service.generate(prompt)
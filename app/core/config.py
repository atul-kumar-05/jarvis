import os
from dataclasses import dataclass


@dataclass(slots=True)
class LlmConfig:
    model: str = os.getenv("OLLAMA_MODEL", "tinyllama:latest")
    temp: float = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))
    max_retries: int = int(os.getenv("OLLAMA_MAX_RETRIES", "3"))
    timeout: float = float(os.getenv("OLLAMA_TIMEOUT", "5"))

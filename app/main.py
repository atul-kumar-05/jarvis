"""
Jarvis — FastAPI application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import action_router, task_router, voice_router
from app.config import llama  # Initialize LlamaIndex settings (Ollama + local embeddings)
from app.core.logging import logger
from app.schemas.task import HealthResponse


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("🚀 Jarvis is starting up...")
    yield
    logger.info("👋 Jarvis is shutting down...")


app = FastAPI(
    title="Jarvis Agent Framework",
    description="Intelligent multi-agent task execution system with voice commands and smart recommendations.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(action_router)
app.include_router(voice_router)


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(version="2.0.0")
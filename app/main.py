"""
Jarvis — FastAPI application entry point.

Configures CORS, registers routers, and provides health/startup hooks.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import logger
from app.dto.dto import HealthResponse
from app.routers.routers import action_router, router as task_router


# ── Lifespan (startup / shutdown) ──────────────────────────────────

@asynccontextmanager
async def lifespan(application: FastAPI):
    """Application startup and shutdown hooks."""
    logger.info("🚀 Jarvis is starting up...")
    yield
    logger.info("👋 Jarvis is shutting down...")


# ── Application ────────────────────────────────────────────────────

app = FastAPI(
    title="Jarvis Agent Framework",
    description="Intelligent multi-agent task execution system with LLM-powered planning, execution, and review.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────

app.include_router(task_router)
app.include_router(action_router)


# ── Health Check ───────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse()
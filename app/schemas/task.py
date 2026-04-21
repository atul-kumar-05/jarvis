"""
Task schemas — request/response DTOs for task endpoints.

Follows Spring-style DTO patterns:
  - Enums for constrained fields (TaskStatus, TaskPriority)
  - Separate Request / Response models
  - Field validation with Pydantic validators
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ── Enums ──────────────────────────────────────────────────────────


class TaskStatus(str, Enum):
    """Allowed task statuses — mirrors a Spring @Enumerated field."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class TaskPriority(str, Enum):
    """Task priority levels used by the scoring engine."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ── Request Schemas ────────────────────────────────────────────────


class TaskCreateRequest(BaseModel):
    """Request body for ``POST /tasks``."""
    title: str = Field(
        ..., min_length=1, max_length=255,
        description="Short, descriptive title of the task",
        examples=["Analyze sales data"],
    )
    description: str = Field(
        ..., min_length=1, max_length=2000,
        description="Detailed description of what the task involves",
        examples=["Process Q4 sales data and generate a summary report"],
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Initial status (defaults to 'pending')",
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Priority level used by the scoring engine",
    )

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "Analyze Sales Data",
                "description": "Process Q4 sales data and generate a summary report",
                "status": "pending",
                "priority": "high",
            }]
        }
    }


class TaskUpdateRequest(BaseModel):
    """Request body for ``PATCH /tasks/{id}``. All fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            return value.strip()
        return value


class GoalRequest(BaseModel):
    """Request body for generating tasks from a goal."""
    goal: str = Field(
        ..., min_length=1, max_length=500,
        description="High-level goal to break into tasks",
        examples=["Build a production-ready AI agent system"],
    )


# ── Response Schemas ───────────────────────────────────────────────


class TaskResponse(BaseModel):
    """Response body returned by task endpoints."""
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    """Wrapper for list endpoints — provides count for convenience."""
    count: int
    tasks: list[TaskResponse]


class ActionResponse(BaseModel):
    """Response for the /next-action endpoint."""
    task_id: Optional[int] = None
    plan: Optional[str] = None
    result: Optional[str] = None
    review: Optional[str] = None
    message: str = "Success"


class DeleteResponse(BaseModel):
    """Response for delete operations."""
    message: str
    deleted_id: int
    deleted_title: str


class RecommendationResponse(BaseModel):
    """Jarvis's smart task recommendation."""
    recommended_task: Optional[TaskResponse] = None
    reason: str = Field(..., description="Why Jarvis recommends this task")
    score: Optional[int] = None
    spoken_recommendation: str = Field(..., description="What Jarvis says aloud")
    pending_count: int = 0


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    status_code: int = 500
    error_type: str = "InternalServerError"


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "2.0.0"

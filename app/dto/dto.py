"""
Data Transfer Objects (DTOs) for the Jarvis API.

Follows Spring-style DTO patterns:
  - Enums for constrained fields (status, priority)
  - Separate Request / Response models
  - Field validation with Pydantic validators
  - Descriptive names: TaskCreateRequest, TaskResponse, etc.
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


class VoiceIntent(str, Enum):
    """Recognized voice command intents."""
    ADD_TASK = "add_task"
    DELETE_TASK = "delete_task"
    NEXT_ACTION = "next_action"
    LIST_TASKS = "list_tasks"
    COMPLETE_TASK = "complete_task"
    TASK_STATUS = "task_status"
    HELP = "help"
    UNKNOWN = "unknown"


# ── Request DTOs ───────────────────────────────────────────────────


class TaskCreateRequest(BaseModel):
    """
    Request body for ``POST /tasks``.
    Equivalent to a Spring ``@RequestBody TaskCreateDTO``.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Short, descriptive title of the task",
        examples=["Analyze sales data"],
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=2000,
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

    # Spring-style validation — strip whitespace from strings
    @field_validator("title", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Analyze Sales Data",
                    "description": "Process Q4 sales data and generate a summary report",
                    "status": "pending",
                    "priority": "high",
                }
            ]
        }
    }


class TaskUpdateRequest(BaseModel):
    """
    Request body for ``PATCH /tasks/{id}``.
    All fields optional — only provided fields are updated.
    """
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
        ...,
        min_length=1,
        max_length=500,
        description="High-level goal to break into tasks",
        examples=["Build a production-ready AI agent system"],
    )


class VoiceCommandRequest(BaseModel):
    """
    Request body for ``POST /voice/command``.
    Accepts a text command (from speech-to-text) and processes it.
    """
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Transcribed voice command text",
        examples=["add task buy groceries with high priority"],
    )

    @field_validator("text", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


# ── Response DTOs ──────────────────────────────────────────────────


class TaskResponse(BaseModel):
    """
    Response body returned by task endpoints.
    Equivalent to a Spring ``ResponseEntity<TaskResponseDTO>``.
    """
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


class VoiceResponse(BaseModel):
    """
    Response from the voice command processor.
    Includes the spoken response text that Jarvis will say aloud.
    """
    intent: VoiceIntent
    spoken_response: str = Field(
        ..., description="The text Jarvis speaks back to the user"
    )
    task: Optional[TaskResponse] = None
    tasks: Optional[list[TaskResponse]] = None
    success: bool = True


class RecommendationResponse(BaseModel):
    """
    Jarvis's smart task recommendation — tells the user what to do next.
    """
    recommended_task: Optional[TaskResponse] = None
    reason: str = Field(
        ..., description="Why Jarvis recommends this task"
    )
    score: Optional[int] = None
    spoken_recommendation: str = Field(
        ..., description="What Jarvis says aloud to the user"
    )
    pending_count: int = 0


class ErrorResponse(BaseModel):
    """Standard error response — like Spring's @ControllerAdvice output."""
    detail: str
    status_code: int = 500
    error_type: str = "InternalServerError"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": "No pending tasks available",
                    "status_code": 404,
                    "error_type": "NotFound",
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "1.0.0"
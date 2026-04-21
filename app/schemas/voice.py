"""
Voice schemas — request/response DTOs for voice command endpoints.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.task import TaskResponse


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


class VoiceCommandRequest(BaseModel):
    """Request body for ``POST /voice/command``."""
    text: str = Field(
        ..., min_length=1, max_length=1000,
        description="Transcribed voice command text",
        examples=["add task buy groceries with high priority"],
    )

    @field_validator("text", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


class VoiceResponse(BaseModel):
    """Response from the voice command processor."""
    intent: VoiceIntent
    spoken_response: str = Field(..., description="The text Jarvis speaks back")
    task: Optional[TaskResponse] = None
    tasks: Optional[list[TaskResponse]] = None
    success: bool = True

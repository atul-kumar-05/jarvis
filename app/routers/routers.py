"""
Task router — RESTful endpoints for task management.

Follows Spring-style controller patterns:
  - Typed request/response DTOs
  - Proper HTTP status codes
  - Error handling with HTTPException
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.agent.manager import decide_next_action
from app.db.db import get_db
from app.dto.dto import (
    ActionResponse,
    ErrorResponse,
    TaskCreateRequest,
    TaskListResponse,
    TaskResponse,
)
from app.service.task_service import get_all_tasks, save_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def create_task(
    request: TaskCreateRequest,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """
    Create a new task with validated title, description, status, and priority.

    - **title**: 1–255 characters (whitespace trimmed)
    - **description**: 1–2000 characters
    - **status**: One of ``pending``, ``in_progress``, ``completed``, ``failed``, ``skipped``
    - **priority**: One of ``low``, ``medium``, ``high``, ``critical``
    """
    saved = save_task(request, db)
    return TaskResponse.model_validate(saved)


@router.get(
    "",
    response_model=TaskListResponse,
    summary="List all tasks",
)
async def list_tasks(db: Session = Depends(get_db)) -> TaskListResponse:
    """Retrieve all tasks ordered by creation time (newest first)."""
    tasks = get_all_tasks(db)
    return TaskListResponse(
        count=len(tasks),
        tasks=[TaskResponse.model_validate(t) for t in tasks],
    )


# ── Action Router ──────────────────────────────────────────────────

action_router = APIRouter(tags=["Actions"])


@action_router.get(
    "/next-action",
    response_model=ActionResponse,
    summary="Get the next recommended action",
    responses={
        404: {"model": ErrorResponse, "description": "No pending tasks"},
    },
)
async def next_action(db: Session = Depends(get_db)) -> ActionResponse:
    """
    Run the agent pipeline (Planner → Executor → Reviewer) on the
    highest-priority pending task and return the results.
    """
    result = decide_next_action(db)

    if result.get("message") == "No pending tasks available":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending tasks available",
        )

    task_obj = result.get("task")
    return ActionResponse(
        task_id=getattr(task_obj, "id", None),
        plan=result.get("plan"),
        result=result.get("result"),
        review=result.get("review_result"),
        message="Pipeline completed successfully",
    )

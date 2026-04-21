"""Task API router — CRUD endpoints for tasks (Spring: @RestController)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.task import (
    DeleteResponse, ErrorResponse, TaskCreateRequest, TaskListResponse,
    TaskResponse, TaskUpdateRequest,
)
from app.services.task_service import (
    delete_task, get_all_tasks, get_task_by_id, mark_task_completed, save_task, update_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Create a new task",
              responses={422: {"model": ErrorResponse}})
async def create_task(request: TaskCreateRequest, db: Session = Depends(get_db)) -> TaskResponse:
    """Create a new task with validated title, description, status, and priority."""
    return TaskResponse.model_validate(save_task(request, db))


@router.get("", response_model=TaskListResponse, summary="List all tasks")
async def list_tasks(db: Session = Depends(get_db)) -> TaskListResponse:
    """Retrieve all tasks ordered by creation time (newest first)."""
    tasks = get_all_tasks(db)
    return TaskListResponse(count=len(tasks), tasks=[TaskResponse.model_validate(t) for t in tasks])


@router.get("/{task_id}", response_model=TaskResponse, summary="Get a task by ID",
             responses={404: {"model": ErrorResponse}})
async def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    """Retrieve a single task by its ID."""
    task = get_task_by_id(task_id, db)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id={task_id} not found")
    return TaskResponse.model_validate(task)


@router.patch("/{task_id}", response_model=TaskResponse, summary="Update a task",
              responses={404: {"model": ErrorResponse}})
async def update_task_endpoint(task_id: int, request: TaskUpdateRequest, db: Session = Depends(get_db)) -> TaskResponse:
    """Partially update a task. Only provided fields are changed."""
    updated = update_task(task_id, request, db)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id={task_id} not found")
    return TaskResponse.model_validate(updated)


@router.post("/{task_id}/complete", response_model=TaskResponse, summary="Mark a task as completed",
             responses={404: {"model": ErrorResponse}})
async def complete_task_endpoint(task_id: int, db: Session = Depends(get_db)) -> TaskResponse:
    """Mark a task as completed."""
    completed = mark_task_completed(task_id, db)
    if not completed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id={task_id} not found")
    return TaskResponse.model_validate(completed)


@router.delete("/{task_id}", response_model=DeleteResponse, summary="Delete a task by ID",
               responses={404: {"model": ErrorResponse}})
async def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)) -> DeleteResponse:
    """Permanently delete a task by its ID."""
    deleted = delete_task(task_id, db)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id={task_id} not found")
    return DeleteResponse(message="Task deleted successfully", deleted_id=deleted.id, deleted_title=deleted.title)

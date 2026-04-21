"""
Task service — business logic for task management (Spring: @Service).
Uses task_repository for data access and scoring_service for ranking.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.core.logging import logger
from app.memory.behavior import analyze_behavior
from app.models.task import Task
from app.repositories import task_repository
from app.schemas.task import TaskCreateRequest, TaskStatus, TaskUpdateRequest
from app.services.scoring_service import score_task


# ── CREATE ─────────────────────────────────────────────────────────

def save_task(task_data: TaskCreateRequest, db: Session) -> Task:
    """Persist a new task from a validated request DTO."""
    db_task = Task(
        title=task_data.title, description=task_data.description,
        status=task_data.status.value, priority=task_data.priority.value,
    )
    task_repository.save(db_task, db)
    logger.info("Task created: id=%d title='%s'", db_task.id, db_task.title)
    return db_task


def quick_add_task(title: str, db: Session, description: str = "", priority: str = "medium") -> Task:
    """Quick-add a task (used by voice commands)."""
    db_task = Task(title=title, description=description or title, status="pending", priority=priority)
    task_repository.save(db_task, db)
    logger.info("Quick-add task: id=%d title='%s' priority=%s", db_task.id, db_task.title, priority)
    return db_task


# ── READ ───────────────────────────────────────────────────────────

def get_task_by_id(task_id: int, db: Session) -> Optional[Task]:
    return task_repository.find_by_id(task_id, db)

def get_all_tasks(db: Session) -> list[Task]:
    return task_repository.find_all(db)

def get_pending_tasks(db: Session) -> list[Task]:
    return task_repository.find_pending(db)

def find_task_by_title(keyword: str, db: Session) -> Optional[Task]:
    return task_repository.find_by_title(keyword, db)


def get_top_task(db: Session) -> Optional[Task]:
    """Select the highest-scoring pending task."""
    pending = task_repository.find_pending(db)
    if not pending:
        logger.info("No pending tasks available")
        return None
    behavior = analyze_behavior(pending, "pending")
    scored = [(t, score_task(t, behavior)) for t in pending]
    scored.sort(key=lambda p: p[1], reverse=True)
    top = scored[0][0]
    logger.info("Top task selected: id=%d title='%s' score=%d", top.id, top.title, scored[0][1])
    return top


def get_top_task_with_score(db: Session) -> tuple[Optional[Task], int, str]:
    """Like get_top_task but also returns score and human-readable reason."""
    pending = task_repository.find_pending(db)
    if not pending:
        return None, 0, "No pending tasks"
    behavior = analyze_behavior(pending, "pending")
    scored = [(t, score_task(t, behavior)) for t in pending]
    scored.sort(key=lambda p: p[1], reverse=True)
    top_task, top_score = scored[0]

    hour = datetime.now().hour
    reasons = []
    if top_task.priority in ("high", "critical"):
        reasons.append(f"it's {top_task.priority} priority")
    if 6 <= hour <= 12:
        reasons.append("morning is your peak focus time")
    elif 13 <= hour <= 17:
        reasons.append("afternoon is good for steady work")
    if "procrastinating" in behavior.lower():
        reasons.append("you've been skipping tasks lately")
    if "consistent" in behavior.lower():
        reasons.append("you're on a great streak")
    reason = ", ".join(reasons) if reasons else "it's the best match right now"
    return top_task, top_score, reason


# ── UPDATE ─────────────────────────────────────────────────────────

def update_task(task_id: int, update_data: TaskUpdateRequest, db: Session) -> Optional[Task]:
    """Partially update a task."""
    task = task_repository.find_by_id(task_id, db)
    if not task:
        return None
    if update_data.title is not None:
        task.title = update_data.title
    if update_data.description is not None:
        task.description = update_data.description
    if update_data.status is not None:
        task.status = update_data.status.value
    if update_data.priority is not None:
        task.priority = update_data.priority.value
    db.commit()
    db.refresh(task)
    logger.info("Task updated: id=%d", task.id)
    return task


def mark_task_completed(task_id: int, db: Session) -> Optional[Task]:
    """Mark a task as completed."""
    task = task_repository.find_by_id(task_id, db)
    if not task:
        return None
    task.status = TaskStatus.COMPLETED.value
    db.commit()
    db.refresh(task)
    logger.info("Task completed: id=%d title='%s'", task.id, task.title)
    return task


# ── DELETE ─────────────────────────────────────────────────────────

def delete_task(task_id: int, db: Session) -> Optional[Task]:
    """Delete a task by ID. Returns deleted task or None."""
    task = task_repository.find_by_id(task_id, db)
    if not task:
        return None
    logger.info("Deleting task: id=%d title='%s'", task.id, task.title)
    task_repository.delete(task, db)
    return task


def delete_task_by_title(keyword: str, db: Session) -> Optional[Task]:
    """Delete the first task matching a title keyword."""
    task = task_repository.find_by_title(keyword, db)
    if not task:
        return None
    logger.info("Deleting task by title: id=%d title='%s'", task.id, task.title)
    task_repository.delete(task, db)
    return task

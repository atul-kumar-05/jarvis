"""
Task service — full CRUD operations, smart task selection, and recommendations.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.core.logging import logger
from app.dto.dto import TaskCreateRequest, TaskPriority, TaskStatus, TaskUpdateRequest
from app.memory.behavior import analyze_behavior
from app.service.score import score_task
from app.task.models import Task


# ── CREATE ─────────────────────────────────────────────────────────


def save_task(task_data: TaskCreateRequest, db: Session) -> Task:
    """
    Persist a new task to the database.

    Args:
        task_data: Validated request DTO.
        db:        Active SQLAlchemy session.

    Returns:
        The created Task ORM instance (with generated ``id``).
    """
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status.value,
        priority=task_data.priority.value,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    logger.info("Task created: id=%d title='%s'", db_task.id, db_task.title)
    return db_task


def quick_add_task(
    title: str,
    db: Session,
    description: str = "",
    priority: str = "medium",
) -> Task:
    """
    Quick-add a task (used by voice commands and internal callers).

    Args:
        title:       Task title.
        db:          Active SQLAlchemy session.
        description: Optional description (defaults to title).
        priority:    Priority string (default: ``"medium"``).

    Returns:
        The created Task ORM instance.
    """
    db_task = Task(
        title=title,
        description=description or title,
        status="pending",
        priority=priority,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    logger.info("Quick-add task: id=%d title='%s' priority=%s", db_task.id, db_task.title, priority)
    return db_task


# ── READ ───────────────────────────────────────────────────────────


def get_task_by_id(task_id: int, db: Session) -> Optional[Task]:
    """Fetch a single task by ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks(db: Session) -> list[Task]:
    """Return all tasks ordered by creation time (newest first)."""
    return db.query(Task).order_by(Task.created_at.desc()).all()


def get_pending_tasks(db: Session) -> list[Task]:
    """Return all pending tasks."""
    return db.query(Task).filter(Task.status == "pending").all()


def get_top_task(db: Session) -> Optional[Task]:
    """
    Select the highest-scoring pending task.

    Uses the scoring engine which factors in priority, behavior, and
    time-of-day energy levels.

    Returns:
        The top-scored ``Task``, or ``None`` if no pending tasks exist.
    """
    pending_tasks = db.query(Task).filter(Task.status == "pending").all()

    if not pending_tasks:
        logger.info("No pending tasks available")
        return None

    behavior = analyze_behavior(pending_tasks, "pending")

    # NOTE: loop variable is `t` to avoid shadowing the `Task` import
    scored_tasks = [
        (t, score_task(t, behavior))
        for t in pending_tasks
    ]
    scored_tasks.sort(key=lambda pair: pair[1], reverse=True)

    top = scored_tasks[0][0]
    logger.info(
        "Top task selected: id=%d title='%s' score=%d",
        top.id,
        top.title,
        scored_tasks[0][1],
    )
    return top


def get_top_task_with_score(db: Session) -> tuple[Optional[Task], int, str]:
    """
    Like ``get_top_task`` but also returns the score and reason.

    Returns:
        Tuple of (task, score, reason_string).
    """
    pending_tasks = db.query(Task).filter(Task.status == "pending").all()

    if not pending_tasks:
        return None, 0, "No pending tasks"

    behavior = analyze_behavior(pending_tasks, "pending")

    scored_tasks = [
        (t, score_task(t, behavior))
        for t in pending_tasks
    ]
    scored_tasks.sort(key=lambda pair: pair[1], reverse=True)

    top_task, top_score = scored_tasks[0]

    # Build a human-readable reason
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
    """
    Partially update a task.

    Args:
        task_id:     ID of the task to update.
        update_data: Fields to update (only non-None fields are applied).
        db:          Active SQLAlchemy session.

    Returns:
        The updated Task, or ``None`` if not found.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
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
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    task.status = TaskStatus.COMPLETED.value
    db.commit()
    db.refresh(task)
    logger.info("Task completed: id=%d title='%s'", task.id, task.title)
    return task


# ── DELETE ─────────────────────────────────────────────────────────


def delete_task(task_id: int, db: Session) -> Optional[Task]:
    """
    Delete a task by ID.

    Args:
        task_id: ID of the task to delete.
        db:      Active SQLAlchemy session.

    Returns:
        The deleted Task object (for response), or ``None`` if not found.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning("Delete failed: task id=%d not found", task_id)
        return None

    logger.info("Deleting task: id=%d title='%s'", task.id, task.title)
    db.delete(task)
    db.commit()
    return task


def delete_task_by_title(title_keyword: str, db: Session) -> Optional[Task]:
    """
    Delete the first task whose title contains the given keyword.
    Used by voice commands like "delete task buy groceries".

    Args:
        title_keyword: A keyword or phrase to search for in task titles.
        db:            Active SQLAlchemy session.

    Returns:
        The deleted Task, or ``None`` if no match found.
    """
    task = (
        db.query(Task)
        .filter(Task.title.ilike(f"%{title_keyword}%"))
        .first()
    )
    if not task:
        logger.warning("Delete by title failed: no task matching '%s'", title_keyword)
        return None

    logger.info("Deleting task by title match: id=%d title='%s'", task.id, task.title)
    db.delete(task)
    db.commit()
    return task


def find_task_by_title(title_keyword: str, db: Session) -> Optional[Task]:
    """Find a task by title keyword match."""
    return (
        db.query(Task)
        .filter(Task.title.ilike(f"%{title_keyword}%"))
        .first()
    )
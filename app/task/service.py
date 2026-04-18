"""
Task service — create tasks from planner output or goals.
"""

from app.core.logging import logger
from app.db.db import SessionLocal
from app.task.models import Task


def create_task(title: str, priority: str = "medium", description: str = "") -> Task:
    """
    Create and persist a single task.

    Args:
        title:       Task title (required).
        priority:    Priority level string (default: ``"medium"``).
        description: Optional task description.

    Returns:
        The persisted ``Task`` instance.
    """
    db = SessionLocal()
    try:
        db_task = Task(
            title=title,
            description=description or title,
            status="pending",
            priority=priority,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        logger.info("Task created from plan: id=%d title='%s'", db_task.id, db_task.title)
        return db_task
    except Exception as exc:
        db.rollback()
        logger.error("Failed to create task '%s': %s", title, exc)
        raise
    finally:
        db.close()


def create_tasks_from_plan(plan_text: str) -> list[Task]:
    """
    Parse a planner's text output and create one task per non-empty line.

    Args:
        plan_text: Multi-line plan text from the planner agent.

    Returns:
        List of created ``Task`` instances.
    """
    tasks: list[Task] = []

    for line in plan_text.strip().split("\n"):
        cleaned = line.strip().lstrip("0123456789.-) ")
        if cleaned:
            task = create_task(title=cleaned, priority="medium")
            tasks.append(task)

    logger.info("Created %d tasks from plan", len(tasks))
    return tasks
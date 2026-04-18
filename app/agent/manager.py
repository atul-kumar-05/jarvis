"""
Agent manager — orchestrates the LangGraph workflow for task execution.
"""

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.core.logging import logger
from app.graph.graph import build_graph
from app.service.task_service import get_top_task

# Build the compiled graph once at module level
_graph = build_graph()


def decide_next_action(db: Session) -> dict[str, Any]:
    """
    Pick the highest-priority pending task and run it through the
    Planner → Executor → Reviewer pipeline.

    Args:
        db: Active SQLAlchemy session for task queries.

    Returns:
        dict with keys ``task``, ``plan``, ``result``, ``review_result``,
        or a message dict if no tasks are available.
    """
    task = get_top_task(db)

    if task is None:
        logger.info("No tasks available for execution")
        return {"message": "No pending tasks available"}

    logger.info("Starting agent pipeline for task: id=%d title='%s'", task.id, task.title)

    try:
        result = _graph.invoke({"task": task})
        logger.info("Agent pipeline completed for task id=%d", task.id)
        return result
    except Exception as exc:
        logger.error("Agent pipeline failed for task id=%d: %s", task.id, exc)
        return {
            "message": f"Pipeline failed: {exc}",
            "task": task,
        }
"""
Behavior tracking module — records task status transitions in memory.
"""

from datetime import datetime
from typing import Any

from app.core.logging import logger

# In-memory behavior log (consider persisting to DB for production)
behavior_log: list[dict[str, Any]] = []


def log_behavior(task: Any, status: str) -> None:
    """Append a behavior entry for the given task and status."""
    behavior_log.append({
        "task": str(task),
        "status": status,
        "time": datetime.now().hour,
    })
    logger.debug("Behavior logged: status=%s, hour=%d", status, datetime.now().hour)


def analyze_behavior(task: Any, status: str) -> str:
    """
    Analyze accumulated behavior to detect patterns.

    Returns a human-readable insight string used by the planner.
    """
    if not behavior_log:
        return "No behavior log — first session"

    skipped = sum(1 for entry in behavior_log if entry["status"] == "skipped")
    completed = sum(1 for entry in behavior_log if entry["status"] == "completed")
    total = len(behavior_log)

    if total > 0 and skipped > completed:
        return f"User is procrastinating (skipped={skipped}, completed={completed})"

    return f"User is consistent (completed={completed}, skipped={skipped})"

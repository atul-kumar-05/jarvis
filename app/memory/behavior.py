"""Behavior tracking module."""

from datetime import datetime
from typing import Any

from app.core.logging import logger

behavior_log: list[dict[str, Any]] = []


def log_behavior(task: Any, status: str) -> None:
    behavior_log.append({"task": str(task), "status": status, "time": datetime.now().hour})
    logger.debug("Behavior logged: status=%s, hour=%d", status, datetime.now().hour)


def analyze_behavior(task: Any, status: str) -> str:
    if not behavior_log:
        return "No behavior log — first session"
    skipped = sum(1 for e in behavior_log if e["status"] == "skipped")
    completed = sum(1 for e in behavior_log if e["status"] == "completed")
    if len(behavior_log) > 0 and skipped > completed:
        return f"User is procrastinating (skipped={skipped}, completed={completed})"
    return f"User is consistent (completed={completed}, skipped={skipped})"

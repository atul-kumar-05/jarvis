"""Task scoring engine — ranks tasks by priority, behavior, and time-of-day."""

from datetime import datetime
from app.core.logging import logger


def score_task(task_obj: object, behavior: str) -> int:
    """Score a task for scheduling priority."""
    score = 0
    priority = getattr(task_obj, "priority", "medium").lower()
    priority_weights = {"critical": 70, "high": 50, "medium": 30, "low": 10}
    score += priority_weights.get(priority, 10)

    if "procrastinating" in behavior.lower():
        score -= 10

    current_hour = datetime.now().hour
    if 6 <= current_hour <= 12:
        score += 20
    elif 13 <= current_hour <= 17:
        score += 10
    elif 18 <= current_hour <= 23:
        score -= 10

    logger.debug("Scored task '%s': %d", getattr(task_obj, "title", "?"), score)
    return score

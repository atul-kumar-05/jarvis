"""
Task scoring engine — ranks tasks by priority, behavior, and time-of-day.
"""

from datetime import datetime

from app.core.logging import logger


def score_task(task_obj: object, behavior: str) -> int:
    """
    Score a task for scheduling priority.

    Factors:
        - Priority level (critical > high > medium > low)
        - User behavior pattern (penalise heavy tasks when procrastinating)
        - Time-of-day energy levels

    Args:
        task_obj: An ORM Task instance with ``priority`` attribute.
        behavior: Behavioral insight string from ``analyze_behavior()``.

    Returns:
        Integer score — higher means "do this first".
    """
    score = 0

    # ── Priority weight ────────────────────────────────────────────
    priority = getattr(task_obj, "priority", "medium").lower()
    priority_weights = {
        "critical": 70,
        "high": 50,
        "medium": 30,
        "low": 10,
    }
    score += priority_weights.get(priority, 10)

    # ── Behavior adjustment ────────────────────────────────────────
    if "procrastinating" in behavior.lower():
        score -= 10  # Avoid heavy tasks for a procrastinating user

    # ── Time-of-day energy window ──────────────────────────────────
    current_hour = datetime.now().hour

    if 6 <= current_hour <= 12:
        score += 20  # Morning deep-work window
    elif 13 <= current_hour <= 17:
        score += 10  # Afternoon — moderate energy
    elif 18 <= current_hour <= 23:
        score -= 10  # Evening — low energy

    logger.debug(
        "Scored task '%s': %d (priority=%s, behavior=%s, hour=%d)",
        getattr(task_obj, "title", "?"),
        score,
        priority,
        behavior[:30],
        current_hour,
    )

    return score
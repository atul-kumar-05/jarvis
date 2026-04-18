"""
Scheduler — generates daily tasks from a configurable goal.
"""

import os

from app.agent.planner import generate_tasks_from_goal
from app.core.logging import logger
from app.task.service import create_tasks_from_plan

# Default goal — can be overridden via environment
DEFAULT_GOAL = os.getenv(
    "DAILY_GOAL",
    "Build a production-ready AI agent system",
)


def daily_goal_planning(goal: str | None = None) -> None:
    """
    Generate and persist tasks from a high-level goal.

    Args:
        goal: Override goal string. Uses ``DAILY_GOAL`` env var if ``None``.
    """
    goal = goal or DEFAULT_GOAL
    logger.info("Starting daily goal planning: '%s'", goal)

    plan = generate_tasks_from_goal(goal)
    tasks = create_tasks_from_plan(plan)

    logger.info("✅ Daily planning complete — %d tasks generated", len(tasks))
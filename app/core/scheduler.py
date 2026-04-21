"""Update the scheduler to use new imports."""

import os
from app.agents.planner import generate_tasks_from_goal
from app.core.logging import logger
from app.config.database import SessionLocal
from app.services.task_service import quick_add_task

DEFAULT_GOAL = os.getenv("DAILY_GOAL", "Build a production-ready AI agent system")


def daily_goal_planning(goal: str | None = None) -> None:
    """Generate and persist tasks from a high-level goal."""
    goal = goal or DEFAULT_GOAL
    logger.info("Starting daily goal planning: '%s'", goal)
    plan = generate_tasks_from_goal(goal)
    db = SessionLocal()
    try:
        tasks = []
        for line in plan.strip().split("\n"):
            cleaned = line.strip().lstrip("0123456789.-) ")
            if cleaned:
                task = quick_add_task(title=cleaned, db=db, priority="medium")
                tasks.append(task)
        logger.info("✅ Daily planning complete — %d tasks generated", len(tasks))
    finally:
        db.close()
"""
Prompt registry — central access point for all prompt templates.
Import prompts from here to avoid scattering import paths.
"""

from app.prompts.planner_prompts import (
    GOAL_PLANNING_PROMPT,
    PLANNER_SYSTEM_PROMPT,
    PLANNER_TASK_PROMPT,
)
from app.prompts.executer_prompts import EXECUTER_PROMPT
from app.prompts.reviewer_prompts import (
    REVIEW_FAILURE_KEYWORDS,
    REVIEW_SUCCESS_KEYWORDS,
    REVIEWER_PROMPT,
)

__all__ = [
    "PLANNER_SYSTEM_PROMPT",
    "PLANNER_TASK_PROMPT",
    "GOAL_PLANNING_PROMPT",
    "EXECUTER_PROMPT",
    "REVIEWER_PROMPT",
    "REVIEW_SUCCESS_KEYWORDS",
    "REVIEW_FAILURE_KEYWORDS",
]

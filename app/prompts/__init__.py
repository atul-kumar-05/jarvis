"""
Prompt registry — central access point for all prompt templates.
Import prompts from ``app.prompts`` directly.
"""

from app.prompts.planner import GOAL_PLANNING_PROMPT, PLANNER_SYSTEM_PROMPT, PLANNER_TASK_PROMPT
from app.prompts.executor import EXECUTOR_PROMPT
from app.prompts.reviewer import REVIEW_FAILURE_KEYWORDS, REVIEW_SUCCESS_KEYWORDS, REVIEWER_PROMPT

__all__ = [
    "PLANNER_SYSTEM_PROMPT", "PLANNER_TASK_PROMPT", "GOAL_PLANNING_PROMPT",
    "EXECUTOR_PROMPT",
    "REVIEWER_PROMPT", "REVIEW_SUCCESS_KEYWORDS", "REVIEW_FAILURE_KEYWORDS",
]

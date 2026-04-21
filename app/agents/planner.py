"""Planner agent — breaks a task into actionable steps using LLM + context."""

from typing import Any
from app.core.logging import logger
from app.llm import generate
from app.memory.behavior import analyze_behavior
from app.memory.rag_service import build_context
from app.prompts.planner import GOAL_PLANNING_PROMPT, PLANNER_TASK_PROMPT


def planner_node(state: dict[str, Any]) -> dict[str, Any]:
    """LangGraph node — generates an execution plan for the current task."""
    task = state["task"]
    behavior = analyze_behavior(task, getattr(task, "status", "pending"))
    context = build_context(task, behavior)
    prompt = PLANNER_TASK_PROMPT.format(task=task, context=context, behavior=behavior)
    plan = generate(prompt)
    logger.info("Plan generated for task: %s", getattr(task, "title", str(task)[:60]))
    return {**state, "plan": plan}


def generate_tasks_from_goal(goal: str) -> str:
    """Generate a list of tasks from a high-level goal."""
    return generate(GOAL_PLANNING_PROMPT.format(goal=goal))

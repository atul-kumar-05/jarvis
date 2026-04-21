"""Executor agent — converts a plan step into a concrete action."""

from typing import Any
from app.core.logging import logger
from app.llm import generate
from app.prompts.executor import EXECUTOR_PROMPT


class ExecutionError(Exception):
    """Raised when the executor receives an empty or invalid plan."""
    pass


def executor_node(state: dict[str, Any]) -> dict[str, Any]:
    """LangGraph node — picks the first plan step and executes it."""
    plan = state.get("plan")
    if not plan:
        raise ExecutionError("Cannot execute — plan is empty or missing")
    logger.info("Executing plan: %s", str(plan)[:100])
    prompt = EXECUTOR_PROMPT.format(plan=plan)
    result = generate(prompt)
    logger.info("Execution result: %s", str(result)[:100])
    return {**state, "result": result}

"""
Executer agent — converts a plan step into a concrete action.
"""

from typing import Any

from app.core.logging import logger
from app.llm import generate
from app.prompts.executer_prompts import EXECUTER_PROMPT


class ExecutionError(Exception):
    """Raised when the executor receives an empty or invalid plan."""
    pass


def executer_node(state: dict[str, Any]) -> dict[str, Any]:
    """
    LangGraph node — picks the first plan step and converts it
    into a concrete action with time estimate.

    Raises:
        ExecutionError: If no plan is available in state.

    Returns:
        Updated state with ``"result"`` key added.
    """
    plan = state.get("plan")

    if not plan:
        raise ExecutionError("Cannot execute — plan is empty or missing")

    logger.info("Executing plan: %s", str(plan)[:100])

    prompt = EXECUTER_PROMPT.format(plan=plan)
    result = generate(prompt)

    logger.info("Execution result: %s", str(result)[:100])

    return {**state, "result": result}
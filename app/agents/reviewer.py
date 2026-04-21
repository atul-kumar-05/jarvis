"""Reviewer agent — evaluates execution quality and stores results in memory."""

from typing import Any
from app.core.logging import logger
from app.llm import generate
from app.memory.behavior import log_behavior
from app.memory.memory_service import store_memory
from app.prompts.reviewer import REVIEW_FAILURE_KEYWORDS, REVIEW_SUCCESS_KEYWORDS, REVIEWER_PROMPT


class ReviewError(Exception):
    pass


def _evaluate_success(review_text: str) -> bool:
    lower = review_text.lower()
    for line in lower.split("\n"):
        if line.strip().startswith("verdict:"):
            verdict = line.split(":", 1)[1].strip()
            if any(kw in verdict for kw in REVIEW_SUCCESS_KEYWORDS):
                return True
            if any(kw in verdict for kw in REVIEW_FAILURE_KEYWORDS):
                return False
    success_hits = sum(1 for kw in REVIEW_SUCCESS_KEYWORDS if kw in lower)
    failure_hits = sum(1 for kw in REVIEW_FAILURE_KEYWORDS if kw in lower)
    return success_hits > failure_hits


def reviewer_node(state: dict[str, Any]) -> dict[str, Any]:
    """LangGraph node — reviews the execution result and stores memory."""
    result = state.get("result")
    if not result:
        raise ReviewError("Cannot review — execution result is empty or missing")
    prompt = REVIEWER_PROMPT.format(result=result)
    review = generate(prompt)
    success = _evaluate_success(review)
    logger.info("Review complete | success=%s | review=%s", success, review[:80])
    store_memory(state["task"], result, review, success)
    log_behavior(state["task"], "completed" if success else "failed")
    return {**state, "review_result": review, "success": success}

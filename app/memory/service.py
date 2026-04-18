"""
Memory service — store and retrieve execution memories via Qdrant.
"""

from datetime import datetime
from typing import Optional

from llama_index.core import Document

from app.core.config import memory_config
from app.core.logging import logger
from app.memory.vector_store import get_index


def _task_to_str(task_obj: object) -> str:
    """Safely convert a task object (ORM model, string, etc.) to a string."""
    if isinstance(task_obj, str):
        return task_obj
    if hasattr(task_obj, "title") and hasattr(task_obj, "description"):
        return f"{task_obj.title} — {task_obj.description}"
    return str(task_obj)


def store_memory(task_obj: object, result: str, review: str, success: bool) -> None:
    """
    Persist an execution memory into the vector store.

    Args:
        task_obj: The task (ORM model or string).
        result:   The execution result text.
        review:   The reviewer's feedback.
        success:  Whether the execution was deemed successful.
    """
    task_str = _task_to_str(task_obj)

    doc = Document(
        text=(
            f"Task: {task_str}\n"
            f"Result: {result}\n"
            f"Review: {review}\n"
            f"Success: {success}"
        ),
        metadata={
            "review": str(review),
            "success": str(success),
            "result": str(result)[:200],
            "timestamp": datetime.now().isoformat(),
            "type": "execution",
        },
    )

    try:
        index = get_index()
        if index is not None:
            index.insert(doc)
            logger.info("Memory stored: %s", task_str[:80])
        else:
            logger.warning("Skipped memory storage — vector index unavailable")
    except Exception as exc:
        logger.warning("Failed to store memory: %s", exc)


def retrieve_memory(query: object) -> str:
    """
    Retrieve relevant past memories using semantic search.

    Args:
        query: A search query (string or task object).

    Returns:
        Stringified retrieval result, or a fallback message.
    """
    query_str = _task_to_str(query)

    try:
        index = get_index()
        if index is None:
            return "No past experience available yet. This is the first task."

        query_engine = index.as_query_engine(
            similarity_top_k=memory_config.top_k,
        )
        result = query_engine.query(query_str)
        return str(result)
    except Exception as exc:
        logger.warning("Memory retrieval failed: %s", exc)
        return f"Unable to retrieve past experience: {exc}"


def rank_memory(memory: str) -> str:
    """Rank / tag memory based on success status keywords."""
    if "failed" in memory.lower():
        return f"[FAILED] {memory}"
    return memory
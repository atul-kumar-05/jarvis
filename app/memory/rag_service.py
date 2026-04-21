"""RAG service — builds context for the planner."""

from app.memory.memory_service import rank_memory, retrieve_memory


def build_context(task: object, behavior: str) -> str:
    """Build a context string for the planner agent."""
    raw_memory = retrieve_memory(task)
    ranked_memory = rank_memory(raw_memory)
    return f"Past Experience:\n{ranked_memory}\n\nBehavioral Pattern:\n{behavior}"

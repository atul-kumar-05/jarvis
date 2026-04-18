from app.memory.service import rank_memory, retrieve_memory


def build_context(task: object, behavior: str) -> str:
    """
    Build a context string for the planner agent.

    Args:
        task:     The current task (ORM model or string).
        behavior: Behavioral insight from ``analyze_behavior()``.

    Returns:
        Formatted context string with past experience and behavior.
    """
    raw_memory = retrieve_memory(task)
    ranked_memory = rank_memory(raw_memory)

    return (
        f"Past Experience:\n{ranked_memory}\n\n"
        f"Behavioral Pattern:\n{behavior}"
    )

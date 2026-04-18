"""
LangGraph workflow — defines the Planner → Executor → Reviewer pipeline.
"""

from typing import Any, Optional

from langgraph.graph import StateGraph

from app.agent.executer import executer_node
from app.agent.planner import planner_node
from app.agent.reviewer import reviewer_node

# ── State schema ───────────────────────────────────────────────────
# Using a plain dict for LangGraph state; keys are documented here:
#   task          — the Task ORM model being processed
#   plan          — planner output (str)
#   result        — executor output (str)
#   review_result — reviewer output (str)
#   success       — bool from the reviewer


def build_graph():
    """
    Construct and compile the agent workflow graph.

    Flow::

        [planner] ──→ [executor] ──→ [reviewer] ──→ END

    Returns:
        A compiled LangGraph ``CompiledGraph`` ready for ``.invoke()``.
    """
    graph = StateGraph(dict)

    graph.add_node("planner", planner_node)
    graph.add_node("executor", executer_node)
    graph.add_node("reviewer", reviewer_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "reviewer")
    graph.set_finish_point("reviewer")

    return graph.compile()
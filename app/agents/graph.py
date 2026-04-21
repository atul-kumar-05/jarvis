"""LangGraph workflow — Planner → Executor → Reviewer pipeline."""

from langgraph.graph import StateGraph
from app.agents.planner import planner_node
from app.agents.executor import executor_node
from app.agents.reviewer import reviewer_node


def build_graph():
    """Construct and compile the agent workflow graph."""
    graph = StateGraph(dict)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("reviewer", reviewer_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "reviewer")
    graph.set_finish_point("reviewer")
    return graph.compile()

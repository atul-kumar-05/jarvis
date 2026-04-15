from langchain_community.chains import graph_qa
from langgraph.graph import StateGraph
from app.agent.planner import planner_node
from app.agent.executer import executer_node
from app.agent.reviewer import reviewer_node

graph = StateGraph(dict)

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("planner",planner_node)
    graph.add_node("executor",executer_node)
    graph.add_node("reviewer",reviewer_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner","executor")
    graph.add_edge('executor','reviewer')
    graph.set_finish_point('executor')

    return graph.compile()
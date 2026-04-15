# domains/agent/manager.py
from sqlalchemy.orm import Session
from app.service.task_service import get_top_task
from app.graph.graph import build_graph

graph = build_graph()
def decide_next_action(db : Session):
    task = get_top_task(db)

    if not task:
        return "No tasks available"

    result = graph.invoke({
        "task": task
    })

    return result
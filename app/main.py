from fastapi import FastAPI

from app.agent.brain import decide_next_action
from app.memory.store import get_memory
from app.task.store import get_tasks

app = FastAPI()


@app.get("/next-action")
def next_action():
    tasks = get_tasks()
    memory = get_memory()
    decision = decide_next_action(tasks, memory)
    return {"decision": decision}
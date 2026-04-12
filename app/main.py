from fastapi import FastAPI

from app.agent.brain import decide_next_action
from app.memory.store import get_memory
from app.task.store import get_tasks
from dbconfig.db import Session
from task.models import Task

app = FastAPI()
db = Session()


@app.get("/next-action")
@async def next_action():
    tasks = get_tasks()
    memory = get_memory()
    decision = decide_next_action(tasks, memory)
    return {"decision": decision}

@app.post("/tasks")
@async def add_task(title: str):
    task = Task(title=title)
    db.add(task)

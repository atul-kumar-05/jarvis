from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.dto.dto import add_task
from app.service.task_service import save_task
from app.agent.manager import decide_next_action
from app.memory.service import retrieve_memory,store_memory

app = FastAPI()

@app.get("/tasks")
@app.get("/next-action")
async def next_action(db : Session = Depends(get_db)):
    tasks = decide_next_action(db)
    return {"tasks": tasks}

@app.post("/tasks")
async def add_task(task: add_task, db: Session = Depends(get_db)):
    saved_task = save_task(task, db)
    return {"task": saved_task}
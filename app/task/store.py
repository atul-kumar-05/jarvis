from db.db import SessionLocal
from app.task.models import task

def get_tasks():
    db = SessionLocal()
    tasks = db.query(task).filter(task.status == 'pending').all()
    return tasks
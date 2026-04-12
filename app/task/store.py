from app.dbconfig.db import Session
from app.task.models import Task

def get_tasks():
    db = Session()
    tasks = db.query(Task).filter(Task.status == 'PENDING').all()
    return tasks
from sqlalchemy.orm import Session
from app.dto.dto import add_task
from app.task.models import task
from app.service.score import score_task
from app.memory.behavior import analyze_behavior


def save_task(task_data: add_task, db: Session):
    db_task = task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

def get_top_task(db : Session):
    pending_tasks = (db.query(task).filter(task.status == 'pending').all())
    behavior = analyze_behavior(pending_tasks,'pending')

    scored_task = [(task, score_task(task, behavior)) for task in pending_tasks]
    scored_task = sorted(scored_task, key=lambda x: x[1], reverse=True)
    return scored_task[0][0]
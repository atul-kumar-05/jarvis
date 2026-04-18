"""
Task store — low-level database queries for tasks.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.db.db import SessionLocal
from app.task.models import Task


def get_pending_tasks(db: Optional[Session] = None) -> list[Task]:
    """
    Fetch all pending tasks.

    Args:
        db: Optional session. If ``None``, creates and closes its own.
    """
    owns_session = db is None
    if owns_session:
        db = SessionLocal()

    try:
        return db.query(Task).filter(Task.status == "pending").all()
    finally:
        if owns_session:
            db.close()
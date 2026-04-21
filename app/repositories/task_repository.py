"""
Task repository — pure data access layer (Spring: @Repository).
Handles all direct database queries for tasks.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.task import Task


def find_all(db: Session) -> list[Task]:
    """Return all tasks ordered by creation time (newest first)."""
    return db.query(Task).order_by(Task.created_at.desc()).all()


def find_by_id(task_id: int, db: Session) -> Optional[Task]:
    """Find a task by primary key."""
    return db.query(Task).filter(Task.id == task_id).first()


def find_pending(db: Session) -> list[Task]:
    """Return all tasks with status 'pending'."""
    return db.query(Task).filter(Task.status == "pending").all()


def find_by_title(keyword: str, db: Session) -> Optional[Task]:
    """Find the first task whose title contains the keyword (case-insensitive)."""
    return db.query(Task).filter(Task.title.ilike(f"%{keyword}%")).first()


def save(task: Task, db: Session) -> Task:
    """Insert or update a task."""
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete(task: Task, db: Session) -> None:
    """Delete a task from the database."""
    db.delete(task)
    db.commit()

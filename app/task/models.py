"""
SQLAlchemy ORM models for tasks and goals.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

from app.db.db import engine

Base = declarative_base()


class Task(Base):
    """Persistent task entity — maps to the ``task`` table."""

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    priority = Column(String, nullable=False, default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"status='{self.status}', priority='{self.priority}')"
        )


class Goal:
    """In-memory goal object used by the scheduler."""

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"Goal(title='{self.title}')"


# Create tables on import (dev convenience — use Alembic in production)
Base.metadata.create_all(engine)
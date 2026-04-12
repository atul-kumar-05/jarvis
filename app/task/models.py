from sqlalchemy import Column,Integer, String, UUID
from sqlalchemy.orm import declarative_base
from app.dbconfig.db import engine

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)

Base.metadata.create_all(engine)
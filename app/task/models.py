from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import declarative_base
from app.db.db import engine

Base = declarative_base()

class task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    priority = Column(String)

Base.metadata.create_all(engine)
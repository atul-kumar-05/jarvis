from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://admin:admi@localhost:5342/agentdb'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
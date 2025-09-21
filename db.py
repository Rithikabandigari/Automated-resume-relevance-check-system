# db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class JobDescription(Base):
    __tablename__ = "jds"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="")
    raw_text = Column(Text)

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    raw_text = Column(Text)

class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    jd_id = Column(Integer)
    resume_id = Column(Integer)
    hard = Column(Float)
    soft = Column(Float)
    llm = Column(Float)
    final_score = Column(Integer)
    verdict = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)

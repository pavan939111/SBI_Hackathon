"""
SQLAlchemy ORM models representing metadata sessions tracking LangGraph runs.
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from app.db.postgres import Base
import datetime

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    langgraph_thread_id = Column(String, unique=True, nullable=False)
    channel = Column(String, default="whatsapp")
    language = Column(String, default="te")
    risk_tier = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

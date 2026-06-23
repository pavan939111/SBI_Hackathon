"""
SQLAlchemy ORM model defining transaction steps in audit logs.
"""
from sqlalchemy import Column, String, Integer, Boolean, JSON, DateTime
from app.db.postgres import Base
import datetime

class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(String, primary_key=True)
    session_id = Column(String)
    customer_id = Column(String)
    agent_name = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    action_detail = Column(JSON)
    risk_tier = Column(Integer, nullable=False)
    autonomous = Column(Boolean, default=False)
    outcome = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

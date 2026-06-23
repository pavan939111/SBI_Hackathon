"""
SQLAlchemy ORM model defining Digital Maturity score indicators.
"""
from sqlalchemy import Column, String, Integer, JSON, DateTime
from app.db.postgres import Base
import datetime

class DMSTrackerModel(Base):
    __tablename__ = "dms_tracker"
    
    id = Column(String, primary_key=True)
    customer_id = Column(String, unique=True, nullable=False)
    current_level = Column(Integer, default=0)
    level_history = Column(JSON)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

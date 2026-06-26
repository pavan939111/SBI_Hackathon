"""
SQLAlchemy ORM models representing customer grievance records.
"""
from sqlalchemy import Column, String, DateTime
from app.db.postgres import Base
import datetime
import uuid

class Grievance(Base):
    __tablename__ = "grievances"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String)
    category = Column(String, nullable=False)
    details = Column(String, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.status is None:
            self.status = "open"


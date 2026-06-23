"""
SQLAlchemy ORM models representing banking scheme definitions details.
"""
from sqlalchemy import Column, String, Float, JSON
from app.db.postgres import Base

class Scheme(Base):
    __tablename__ = "schemes"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    max_amount = Column(Float)
    interest_rate_percent = Column(Float)
    eligibility_rules = Column(JSON)

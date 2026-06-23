"""
SQLAlchemy ORM models representing profile parameters for customers.
"""
from sqlalchemy import Column, String, Integer, DateTime
from app.db.postgres import Base
import datetime

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    name = Column(String)
    sbi_account_number = Column(String)
    kyc_occupation = Column(String)
    dms_level = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

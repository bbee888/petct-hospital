from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Date, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    site_domain = Column(String(255), nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.id', ondelete='CASCADE'), nullable=False)
    username = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    idcard = Column(String(30), nullable=False)
    sex = Column(String(10), nullable=False)
    appoint_date = Column(Date, nullable=False)
    intro = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Integer, default=0)
    
    hospital = relationship("Hospital")

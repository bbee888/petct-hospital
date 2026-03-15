from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.db.base import Base

class Site(Base):
    __tablename__ = "sites"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    domain = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    logo = Column(String(500), nullable=True)
    seo_title = Column(String(100), nullable=True)
    seo_keywords = Column(String(120), nullable=True)
    seo_description = Column(String(255), nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

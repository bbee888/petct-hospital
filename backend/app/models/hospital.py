from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.tag import hospital_tags

class Hospital(Base):
    __tablename__ = "hospitals"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    site_domain = Column(String(255), nullable=False, index=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    level = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    seo_keywords = Column(String(200), nullable=True)
    seo_description = Column(String(255), nullable=True)
    seo_title = Column(String(100), nullable=True)
    price = Column(Integer, nullable=True)
    device = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)
    advantage = Column(Text, nullable=True)
    ks_intro = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    cover = Column(String(200), nullable=True)
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    
    tags = relationship("Tag", secondary=hospital_tags, backref="hospitals")

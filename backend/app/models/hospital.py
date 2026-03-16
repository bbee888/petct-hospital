from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province_id = Column(Integer, ForeignKey('provinces.id', ondelete='CASCADE'), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(100), nullable=False)
    level = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    device = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)
    advantage = Column(Text, nullable=True)
    ks_intro = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    cover = Column(String(200), nullable=True)
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    seo_title = Column(String(100), nullable=True)
    tags = Column(String(100), nullable=True)
    seo_description = Column(String(255), nullable=True)

    # 关系
    province = relationship("Province", back_populates="hospitals")
    city = relationship("City", back_populates="hospitals")


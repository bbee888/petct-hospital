from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.tag import article_tags

class ArticleCategory(Base):
    __tablename__ = "article_categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    site_domain = Column(String(255), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    
    articles = relationship("Article", back_populates="category")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    site_domain = Column(String(255), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey('article_categories.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(100), nullable=False)
    seo_keywords = Column(String(120), nullable=True)
    seo_description = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    cover = Column(String(100), nullable=True)
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True), server_default=func.now())
    
    category = relationship("ArticleCategory", back_populates="articles")
    tags = relationship("Tag", secondary=article_tags, backref="articles")

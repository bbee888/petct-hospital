from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ArticleCategoryBase(BaseModel):
    name: str
    slug: str
    site_domain: str

class ArticleCategoryCreate(ArticleCategoryBase):
    pass

class ArticleCategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    site_domain: Optional[str] = None

class ArticleCategory(ArticleCategoryBase):
    id: int
    site_domain: str
    
    class Config:
        from_attributes = True

class ArticleBase(BaseModel):
    title: str
    category_id: int
    description: Optional[str] = None
    content: str
    cover: Optional[str] = None
    tags: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    content: Optional[str] = None
    cover: Optional[str] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None

class Article(ArticleBase):
    id: int
    view_count: int
    is_published: bool
    published_at: datetime

    class Config:
        from_attributes = True

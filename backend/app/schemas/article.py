from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ArticleCategoryBase(BaseModel):
    name: str
    slug: str

class ArticleCategoryCreate(ArticleCategoryBase):
    pass

class ArticleCategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None

class ArticleCategory(ArticleCategoryBase):
    id: int
    site_domain: str
    
    class Config:
        from_attributes = True

class ArticleBase(BaseModel):
    title: str
    category_id: int
    seo_keywords: str | None = None
    seo_description: str | None = None
    content: str
    cover: str | None = None
    tags: str | None = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    is_published: bool | None = None

class Article(ArticleBase):
    id: int
    site_domain: str
    view_count: int
    is_published: bool
    published_at: datetime
    
    class Config:
        from_attributes = True

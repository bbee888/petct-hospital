from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SiteBase(BaseModel):
    domain: str
    name: str
    logo: Optional[str] = None
    seo_title: Optional[str] = None
    seo_keywords: Optional[str] = None
    seo_description: Optional[str] = None

class SiteCreate(SiteBase):
    pass

class SiteUpdate(BaseModel):
    domain: Optional[str] = None
    name: Optional[str] = None
    logo: Optional[str] = None
    seo_title: Optional[str] = None
    seo_keywords: Optional[str] = None
    seo_description: Optional[str] = None
    status: Optional[bool] = None

class Site(SiteBase):
    id: int
    status: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

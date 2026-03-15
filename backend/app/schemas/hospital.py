from pydantic import BaseModel
from datetime import datetime

class HospitalBase(BaseModel):
    name: str
    level: str | None = None
    phone: str | None = None
    city_id: int
    seo_keywords: str | None = None
    seo_description: str | None = None
    seo_title: str | None = None
    price: int | None = None
    device: str | None = None
    address: str | None = None
    advantage: str | None = None
    ks_intro: str | None = None
    content: str | None = None
    cover: str | None = None
    tags: str | None = None

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdate(HospitalBase):
    is_published: bool | None = None

class Hospital(HospitalBase):
    id: int
    site_domain: str
    view_count: int
    is_published: bool
    published_at: datetime
    
    class Config:
        from_attributes = True

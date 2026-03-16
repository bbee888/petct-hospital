from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HospitalBase(BaseModel):
    title: str
    province_id: int
    city_id: int
    level: str
    seo_title: Optional[str] = None
    tags: Optional[str] = None
    seo_description: Optional[str] = None
    price: Optional[int] = None
    device: Optional[str] = None
    address: Optional[str] = None
    advantage: Optional[str] = None
    ks_intro: Optional[str] = None
    content: Optional[str] = None
    cover: Optional[str] = None

class HospitalCreate(HospitalBase):
    pass

class HospitalUpdate(HospitalBase):
    is_published: Optional[bool] = None

class Hospital(HospitalBase):
    id: int
    view_count: int
    is_published: bool
    create_at: datetime
    province_name: Optional[str] = None
    city_name: Optional[str] = None

    class Config:
        from_attributes = True

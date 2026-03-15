from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class AppointmentBase(BaseModel):
    hospital_id: int
    username: str
    phone: str
    idcard: str
    sex: str
    appoint_date: date
    intro: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    status: Optional[int] = None

class Appointment(AppointmentBase):
    id: int
    site_domain: str
    created_at: datetime
    status: int
    hospital_name: Optional[str] = None
    
    class Config:
        from_attributes = True

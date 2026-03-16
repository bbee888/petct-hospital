from pydantic import BaseModel
from typing import Optional

class StatsResponse(BaseModel):
    sites_count: int
    hospitals_count: int
    articles_count: int
    appointments_count: int
    users_count: int
    
    # 趋势数据 (环比)
    sites_trend: Optional[float] = None
    hospitals_trend: Optional[float] = None
    articles_trend: Optional[float] = None
    appointments_trend: Optional[float] = None
    users_trend: Optional[float] = None

class AppointmentStatsResponse(BaseModel):
    pending_count: int
    confirmed_count: int
    completed_count: int
    cancelled_count: int

class RecentAppointmentItem(BaseModel):
    id: int
    username: str
    phone: str
    appoint_date: str
    hospital_name: str
    status: str

class RecentAppointmentsResponse(BaseModel):
    appointments: list[RecentAppointmentItem]

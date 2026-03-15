from pydantic import BaseModel
from typing import Optional, List

class ProvinceBase(BaseModel):
    name: str
    sort: Optional[int] = 0

class ProvinceCreate(ProvinceBase):
    pass

class ProvinceUpdate(BaseModel):
    name: Optional[str] = None
    sort: Optional[int] = None

class Province(ProvinceBase):
    id: int
    
    class Config:
        from_attributes = True

class CityBase(BaseModel):
    province_id: int
    name: str

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    province_id: Optional[int] = None
    name: Optional[str] = None

class City(CityBase):
    id: int
    
    class Config:
        from_attributes = True

class DistrictBase(BaseModel):
    city_id: int
    name: str

class DistrictCreate(DistrictBase):
    pass

class DistrictUpdate(BaseModel):
    city_id: Optional[int] = None
    name: Optional[str] = None

class District(DistrictBase):
    id: int
    
    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Province(Base):
    __tablename__ = "provinces"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    sort = Column(Integer, nullable=False, default=0)
    
    cities = relationship("City", back_populates="province")

class City(Base):
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province_id = Column(Integer, ForeignKey('provinces.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    
    province = relationship("Province", back_populates="cities")
    districts = relationship("District", back_populates="city")

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    
    city = relationship("City", back_populates="districts")

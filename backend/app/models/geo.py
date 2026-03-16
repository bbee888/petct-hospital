from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    cities = relationship("City", back_populates="province")
    hospitals = relationship("Hospital", back_populates="province")

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province_id = Column(Integer, ForeignKey('provinces.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)

    province = relationship("Province", back_populates="cities")
    hospitals = relationship("Hospital", back_populates="city")
    districts = relationship("District", back_populates="city")

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey('cities.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    
    city = relationship("City", back_populates="districts")

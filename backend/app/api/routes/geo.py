from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.geo import Province, City, District
from app.schemas.geo import ProvinceCreate, ProvinceUpdate, Province as ProvinceSchema, CityCreate, CityUpdate, City as CitySchema, DistrictCreate, DistrictUpdate, District as DistrictSchema
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class DistrictTreeNode(BaseModel):
    id: int
    name: str
    type: str = "district"

class CityTreeNode(BaseModel):
    id: int
    name: str
    type: str = "city"
    children: List[DistrictTreeNode] = []

class ProvinceTreeNode(BaseModel):
    id: int
    name: str
    sort: Optional[int] = 0
    type: str = "province"
    children: List[CityTreeNode] = []

# 省份相关路由
@router.get("/provinces", response_model=list[ProvinceSchema])
async def get_provinces(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Province).order_by(Province.sort, Province.id))
    provinces = result.scalars().all()
    return provinces

@router.post("/provinces", response_model=ProvinceSchema)
async def create_province(
    province: ProvinceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_province = Province(**province.model_dump())
    db.add(db_province)
    await db.commit()
    await db.refresh(db_province)
    return db_province

@router.get("/provinces/{province_id}", response_model=ProvinceSchema)
async def get_province(
    province_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Province).where(Province.id == province_id))
    province = result.scalars().first()
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found"
        )
    return province

@router.put("/provinces/{province_id}", response_model=ProvinceSchema)
async def update_province(
    province_id: int,
    province: ProvinceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Province).where(Province.id == province_id))
    db_province = result.scalars().first()
    if not db_province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found"
        )
    
    update_data = province.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_province, field, value)
    
    await db.commit()
    await db.refresh(db_province)
    return db_province

@router.delete("/provinces/{province_id}")
async def delete_province(
    province_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Province).where(Province.id == province_id))
    province = result.scalars().first()
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found"
        )
    
    # 检查是否有关联的城市
    result = await db.execute(select(City).where(City.province_id == province_id))
    cities = result.scalars().all()
    if cities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete province with existing cities"
        )
    
    await db.delete(province)
    await db.commit()
    return {"message": "Province deleted successfully"}

# 城市相关路由
@router.get("/cities", response_model=list[CitySchema])
async def get_cities(
    province_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(City)
    if province_id:
        query = query.where(City.province_id == province_id)
    query = query.order_by(City.id)
    result = await db.execute(query)
    cities = result.scalars().all()
    return cities

@router.post("/cities", response_model=CitySchema)
async def create_city(
    city: CityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 验证省份是否存在
    result = await db.execute(select(Province).where(Province.id == city.province_id))
    province = result.scalars().first()
    if not province:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Province not found"
        )
    
    db_city = City(**city.model_dump())
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city

@router.get("/cities/{city_id}", response_model=CitySchema)
async def get_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalars().first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return city

@router.put("/cities/{city_id}", response_model=CitySchema)
async def update_city(
    city_id: int,
    city: CityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(City).where(City.id == city_id))
    db_city = result.scalars().first()
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    
    # 如果修改了省份，验证省份是否存在
    if city.province_id:
        result = await db.execute(select(Province).where(Province.id == city.province_id))
        province = result.scalars().first()
        if not province:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Province not found"
            )
    
    update_data = city.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_city, field, value)
    
    await db.commit()
    await db.refresh(db_city)
    return db_city

@router.delete("/cities/{city_id}")
async def delete_city(
    city_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalars().first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    
    # 检查是否有关联的区县
    result = await db.execute(select(District).where(District.city_id == city_id))
    districts = result.scalars().all()
    if districts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete city with existing districts"
        )
    
    await db.delete(city)
    await db.commit()
    return {"message": "City deleted successfully"}

# 区县相关路由
@router.get("/districts", response_model=list[DistrictSchema])
async def get_districts(
    city_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = select(District)
    if city_id:
        query = query.where(District.city_id == city_id)
    query = query.order_by(District.id)
    result = await db.execute(query)
    districts = result.scalars().all()
    return districts

@router.post("/districts", response_model=DistrictSchema)
async def create_district(
    district: DistrictCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 验证城市是否存在
    result = await db.execute(select(City).where(City.id == district.city_id))
    city = result.scalars().first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    
    db_district = District(**district.model_dump())
    db.add(db_district)
    await db.commit()
    await db.refresh(db_district)
    return db_district

@router.get("/districts/{district_id}", response_model=DistrictSchema)
async def get_district(
    district_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(District).where(District.id == district_id))
    district = result.scalars().first()
    if not district:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found"
        )
    return district

@router.put("/districts/{district_id}", response_model=DistrictSchema)
async def update_district(
    district_id: int,
    district: DistrictUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(District).where(District.id == district_id))
    db_district = result.scalars().first()
    if not db_district:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found"
        )
    
    # 如果修改了城市，验证城市是否存在
    if district.city_id:
        result = await db.execute(select(City).where(City.id == district.city_id))
        city = result.scalars().first()
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found"
            )
    
    update_data = district.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_district, field, value)
    
    await db.commit()
    await db.refresh(db_district)
    return db_district

@router.delete("/districts/{district_id}")
async def delete_district(
    district_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(District).where(District.id == district_id))
    district = result.scalars().first()
    if not district:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found"
        )
    
    await db.delete(district)
    await db.commit()
    return {"message": "District deleted successfully"}

# 树形结构数据接口
@router.get("/tree", response_model=list[ProvinceTreeNode])
async def get_geo_tree(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(
        select(Province).options(
            selectinload(Province.cities).selectinload(City.districts)
        ).order_by(Province.sort, Province.id)
    )
    provinces = result.scalars().unique().all()
    
    tree_data = []
    for province in provinces:
        province_node = ProvinceTreeNode(
            id=province.id,
            name=province.name,
            sort=province.sort,
            type="province",
            children=[]
        )
        for city in province.cities:
            city_node = CityTreeNode(
                id=city.id,
                name=city.name,
                type="city",
                children=[]
            )
            for district in city.districts:
                district_node = DistrictTreeNode(
                    id=district.id,
                    name=district.name,
                    type="district"
                )
                city_node.children.append(district_node)
            province_node.children.append(city_node)
        tree_data.append(province_node)
    
    return tree_data

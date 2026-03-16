from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.hospital import Hospital
from app.models.geo import Province, City
from app.schemas.hospital import HospitalCreate, HospitalUpdate, Hospital as HospitalSchema

router = APIRouter()

@router.get("/", response_model=List[HospitalSchema])
async def get_hospitals(
    title: Optional[str] = None,
    province_id: Optional[int] = None,
    city_id: Optional[int] = None,
    level: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        query = select(Hospital).options(
            joinedload(Hospital.province),
            joinedload(Hospital.city)
        )

        conditions = []
        if title:
            conditions.append(Hospital.title.like(f"%{title}%"))
        if province_id:
            conditions.append(Hospital.province_id == province_id)
        if city_id:
            conditions.append(Hospital.city_id == city_id)
        if level:
            conditions.append(Hospital.level == level)

        if conditions:
            query = query.where(*conditions)

        result = await db.execute(query)
        hospitals = result.scalars().all()

        # 构造响应数据，添加省份和城市名称
        result_data = []
        for hospital in hospitals:
            hospital_dict = {
                **hospital.__dict__,
                'province_name': hospital.province.name if hospital.province else None,
                'city_name': hospital.city.name if hospital.city else None
            }
            result_data.append(HospitalSchema(**hospital_dict))

        return result_data
    except Exception as e:
        print(f"Error in get_hospitals: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/", response_model=HospitalSchema)
async def create_hospital(
    hospital: HospitalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 验证 title 是否重复
    result = await db.execute(select(Hospital).where(Hospital.title == hospital.title))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hospital with title '{hospital.title}' already exists"
        )

    # 创建医院
    db_hospital = Hospital(**hospital.model_dump())
    db.add(db_hospital)
    await db.commit()
    await db.refresh(db_hospital)

    return db_hospital

@router.get("/{hospital_id}", response_model=HospitalSchema)
async def get_hospital(
    hospital_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )
    return hospital

@router.put("/{hospital_id}", response_model=HospitalSchema)
async def update_hospital(
    hospital_id: int,
    hospital: HospitalUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    db_hospital = result.scalars().first()
    if not db_hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )

    # 如果更新 title，验证是否重复
    if hospital.title and hospital.title != db_hospital.title:
        result = await db.execute(select(Hospital).where(Hospital.title == hospital.title))
        existing = result.scalars().first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Hospital with title '{hospital.title}' already exists"
            )

    # 更新医院
    for field, value in hospital.model_dump(exclude_unset=True).items():
        setattr(db_hospital, field, value)

    await db.commit()
    await db.refresh(db_hospital)

    return db_hospital

@router.delete("/{hospital_id}")
async def delete_hospital(
    hospital_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )

    await db.delete(hospital)
    await db.commit()
    return {"message": "Hospital deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
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

@router.get("/")
async def get_hospitals(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    title: Optional[str] = None,
    province_id: Optional[int] = None,
    city_id: Optional[int] = None,
    level: Optional[str] = None,
    is_cooperation: Optional[int] = None,  # 新增筛选字段
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(get_current_active_user)  # 临时禁用认证用于测试
):
    try:
        # 构建基础查询
        query = select(Hospital).options(
            joinedload(Hospital.province),
            joinedload(Hospital.city)
        )

        # 添加筛选条件
        conditions = []
        if title:
            conditions.append(Hospital.title.like(f"%{title}%"))
        if province_id:
            conditions.append(Hospital.province_id == province_id)
        if city_id:
            conditions.append(Hospital.city_id == city_id)
        if level:
            conditions.append(Hospital.level == level)
        if is_cooperation is not None:
            conditions.append(Hospital.is_cooperation == is_cooperation)

        if conditions:
            query = query.where(*conditions)

        # 获取总数
        total_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0

        # 获取分页数据
        offset = (page - 1) * size
        paginated_query = query.offset(offset).limit(size)
        result = await db.execute(paginated_query)
        hospitals = result.scalars().all()

        # 构造响应数据，添加省份和城市名称
        result_data = []
        for hospital in hospitals:
            # 使用 model_validate 来确保所有字段都被正确包含
            hospital_dict = HospitalSchema.model_validate(hospital).model_dump()
            hospital_dict['province_name'] = hospital.province.name if hospital.province else None
            hospital_dict['city_name'] = hospital.city.name if hospital.city else None
            result_data.append(hospital_dict)

        return {
            "items": result_data,
            "total": total,
            "page": page,
            "size": size
        }
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
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Hospital)
        .options(joinedload(Hospital.province), joinedload(Hospital.city))
        .where(Hospital.id == hospital_id)
    )
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )
    
    # 更新浏览量：增加1-10的随机数
    import random
    view_increment = random.randint(1, 10)
    hospital.view_count = (hospital.view_count or 0) + view_increment
    await db.commit()
    
    # 构造响应数据，添加省份和城市名称
    hospital_dict = HospitalSchema.model_validate(hospital).model_dump()
    hospital_dict['province_name'] = hospital.province.name if hospital.province else None
    hospital_dict['city_name'] = hospital.city.name if hospital.city else None
    
    return hospital_dict

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

# 获取同省合作医院
@router.get("/province/{hospital_id}")
async def get_province_hospitals(
    hospital_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取同省的合作医院推荐"""
    # 先获取当前医院的信息
    result = await db.execute(
        select(Hospital).options(
            joinedload(Hospital.province)
        ).where(Hospital.id == hospital_id)
    )
    current_hospital = result.scalars().first()
    
    if not current_hospital or not current_hospital.province_id:
        return {"items": [], "total": 0}
    
    # 获取同省的合作医院（排除当前医院）
    query = select(Hospital).options(
        joinedload(Hospital.province),
        joinedload(Hospital.city)
    ).where(
        Hospital.province_id == current_hospital.province_id,
        Hospital.id != hospital_id,
        Hospital.is_cooperation == 1
    ).limit(5)
    
    result = await db.execute(query)
    hospitals = result.scalars().unique().all()
    
    result_data = []
    for h in hospitals:
        h_dict = HospitalSchema.model_validate(h).model_dump()
        h_dict['province_name'] = h.province.name if h.province else None
        h_dict['city_name'] = h.city.name if h.city else None
        result_data.append(h_dict)
    
    return {"items": result_data, "total": len(result_data)}

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

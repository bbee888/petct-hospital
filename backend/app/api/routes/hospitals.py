from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate, Hospital as HospitalSchema
from app.services.tag_service import process_tags

router = APIRouter()

@router.get("/", response_model=list[HospitalSchema])
async def get_hospitals(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    try:
        # 检查request.state是否有domain属性
        if not hasattr(request.state, 'domain'):
            # 如果没有，设置默认值
            request.state.domain = "localhost"
            print("Set default domain to localhost")
        
        domain = request.state.domain
        print(f"Domain: {domain}")
        result = await db.execute(select(Hospital).where(Hospital.site_domain == domain))
        hospitals = result.scalars().all()
        print(f"Hospitals found: {len(hospitals)}")
        return hospitals
    except Exception as e:
        print(f"Error in get_hospitals: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/", response_model=HospitalSchema)
async def create_hospital(
    request: Request,
    hospital: HospitalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 检查request.state是否有domain属性
    if not hasattr(request.state, 'domain'):
        # 如果没有，设置默认值
        request.state.domain = "localhost"
    
    domain = request.state.domain
    
    # 创建医院
    db_hospital = Hospital(
        **hospital.model_dump(exclude={"tags"}),
        site_domain=domain
    )
    db.add(db_hospital)
    await db.commit()
    await db.refresh(db_hospital)
    
    # 处理标签
    if hospital.tags:
        await process_tags(db, "hospital", db_hospital.id, hospital.tags)
    
    return db_hospital

@router.get("/{hospital_id}", response_model=HospitalSchema)
async def get_hospital(
    hospital_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 检查request.state是否有domain属性
    if not hasattr(request.state, 'domain'):
        # 如果没有，设置默认值
        request.state.domain = "localhost"
    
    domain = request.state.domain
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id, Hospital.site_domain == domain)
    )
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
    request: Request,
    hospital: HospitalUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 检查request.state是否有domain属性
    if not hasattr(request.state, 'domain'):
        # 如果没有，设置默认值
        request.state.domain = "localhost"
    
    domain = request.state.domain
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id, Hospital.site_domain == domain)
    )
    db_hospital = result.scalars().first()
    if not db_hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )
    
    # 更新医院
    for field, value in hospital.model_dump(exclude_unset=True, exclude={"tags"}).items():
        setattr(db_hospital, field, value)
    
    await db.commit()
    await db.refresh(db_hospital)
    
    # 处理标签
    if hospital.tags is not None:
        await process_tags(db, "hospital", db_hospital.id, hospital.tags)
    
    return db_hospital

@router.delete("/{hospital_id}")
async def delete_hospital(
    hospital_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 检查request.state是否有domain属性
    if not hasattr(request.state, 'domain'):
        # 如果没有，设置默认值
        request.state.domain = "localhost"
    
    domain = request.state.domain
    result = await db.execute(
        select(Hospital).where(Hospital.id == hospital_id, Hospital.site_domain == domain)
    )
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )
    
    await db.delete(hospital)
    await db.commit()
    return {"message": "Hospital deleted successfully"}

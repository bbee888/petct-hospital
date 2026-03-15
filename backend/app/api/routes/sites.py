from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate, Site as SiteSchema

router = APIRouter()

@router.get("/", response_model=list[SiteSchema])
async def get_sites(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Site))
    sites = result.scalars().all()
    return sites

@router.post("/", response_model=SiteSchema)
async def create_site(
    site: SiteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # 检查域名是否已存在
    result = await db.execute(select(Site).where(Site.domain == site.domain))
    existing_site = result.scalars().first()
    if existing_site:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Domain already exists"
        )
    
    # 创建站点
    db_site = Site(**site.model_dump())
    db.add(db_site)
    await db.commit()
    await db.refresh(db_site)
    return db_site

@router.get("/{site_id}", response_model=SiteSchema)
async def get_site(
    site_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalars().first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )
    return site

@router.put("/{site_id}", response_model=SiteSchema)
async def update_site(
    site_id: int,
    site: SiteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Site).where(Site.id == site_id))
    db_site = result.scalars().first()
    if not db_site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )
    
    # 调试：打印接收到的数据
    print(f"接收到的更新数据: {site.model_dump()}")
    
    # 更新站点
    update_data = site.model_dump(exclude_unset=True)
    print(f"排除未设置字段后的数据: {update_data}")
    
    for field, value in update_data.items():
        if value is not None or field in ['seo_title', 'seo_keywords', 'seo_description']:
            setattr(db_site, field, value)
            print(f"更新字段 {field}: {value}")
    
    await db.commit()
    await db.refresh(db_site)
    print(f"保存后的数据: {db_site.seo_title}, {db_site.seo_keywords}, {db_site.seo_description}")
    return db_site

@router.delete("/{site_id}")
async def delete_site(
    site_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalars().first()
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )
    
    await db.delete(site)
    await db.commit()
    return {"message": "Site deleted successfully"}

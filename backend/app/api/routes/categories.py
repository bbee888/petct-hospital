from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, Category as CategorySchema

router = APIRouter()


@router.get("/")
async def get_categories(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Category).order_by(Category.id)
    )
    categories = result.scalars().all()
    return [{
        'id': cat.id,
        'name': cat.name,
        'slug': cat.slug,
        'site_domain': cat.site_domain,
        'created_at': cat.created_at,
        'updated_at': cat.updated_at
    } for cat in categories]


@router.post("/")
async def create_category(
    request: Request,
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    
    # 检查slug是否已存在
    result = await db.execute(
        select(Category).where(Category.slug == category.slug)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    
    db_category = Category(
        name=category.name,
        slug=category.slug,
        site_domain="localhost"
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return {
        'id': db_category.id,
        'name': db_category.name,
        'slug': db_category.slug,
        'site_domain': db_category.site_domain,
        'created_at': db_category.created_at,
        'updated_at': db_category.updated_at
    }


@router.get("/{category_id}")
async def get_category(
    category_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return {
        'id': category.id,
        'name': category.name,
        'slug': category.slug,
        'site_domain': category.site_domain,
        'created_at': category.created_at,
        'updated_at': category.updated_at
    }


@router.put("/{category_id}")
async def update_category(
    category_id: int,
    request: Request,
    category: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    db_category = result.scalars().first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # 检查slug是否已被其他分类使用
    if category.slug != db_category.slug:
        result = await db.execute(
            select(Category).where(Category.slug == category.slug, Category.id != category_id)
        )
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slug already exists"
            )
    
    update_data = category.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    await db.commit()
    await db.refresh(db_category)
    return {
        'id': db_category.id,
        'name': db_category.name,
        'slug': db_category.slug,
        'site_domain': db_category.site_domain,
        'created_at': db_category.created_at,
        'updated_at': db_category.updated_at
    }


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    await db.delete(category)
    await db.commit()
    return {"message": "Category deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.article import Article, ArticleCategory
from app.schemas.article import ArticleCreate, ArticleUpdate, Article as ArticleSchema, ArticleCategoryCreate, ArticleCategoryUpdate, ArticleCategory as ArticleCategorySchema
from app.services.tag_service import process_tags

router = APIRouter()

# 文章分类相关路由
@router.get("/categories", response_model=list[ArticleCategorySchema])
async def get_article_categories(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(select(ArticleCategory))
    categories = result.scalars().all()
    return categories

@router.post("/categories", response_model=ArticleCategorySchema)
async def create_article_category(
    request: Request,
    category: ArticleCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    
    # 创建分类
    db_category = ArticleCategory(
        **category.model_dump(),
        site_domain="localhost"
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.get("/categories/{category_id}", response_model=ArticleCategorySchema)
async def get_article_category(
    category_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(ArticleCategory).where(ArticleCategory.id == category_id)
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.put("/categories/{category_id}", response_model=ArticleCategorySchema)
async def update_article_category(
    category_id: int,
    request: Request,
    category: ArticleCategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(ArticleCategory).where(ArticleCategory.id == category_id)
    )
    db_category = result.scalars().first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # 更新分类
    update_data = category.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}")
async def delete_article_category(
    category_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(ArticleCategory).where(ArticleCategory.id == category_id)
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # 检查是否有关联的文章
    result = await db.execute(
        select(Article).where(Article.category_id == category_id)
    )
    articles = result.scalars().all()
    if articles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with existing articles"
        )
    
    await db.delete(category)
    await db.commit()
    return {"message": "Category deleted successfully"}

# 文章相关路由
@router.get("/", response_model=list[ArticleSchema])
async def get_articles(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(select(Article))
    articles = result.scalars().all()
    return articles

@router.post("/", response_model=ArticleSchema)
async def create_article(
    request: Request,
    article: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    
    # 验证分类是否存在
    result = await db.execute(
        select(ArticleCategory).where(ArticleCategory.id == article.category_id)
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # 创建文章
    db_article = Article(
        **article.model_dump(exclude={"tags"}),
        site_domain="localhost"
    )
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)
    
    # 处理标签
    if article.tags:
        await process_tags(db, "article", db_article.id, article.tags)
    
    return db_article

@router.get("/{article_id}", response_model=ArticleSchema)
async def get_article(
    article_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    return article

@router.put("/{article_id}", response_model=ArticleSchema)
async def update_article(
    article_id: int,
    request: Request,
    article: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Article).where(Article.id == article_id)
    )
    db_article = result.scalars().first()
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # 验证分类是否存在
    if article.category_id:
        result = await db.execute(
            select(ArticleCategory).where(ArticleCategory.id == article.category_id)
        )
        category = result.scalars().first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # 更新文章
    for field, value in article.model_dump(exclude_unset=True, exclude={"tags"}).items():
        setattr(db_article, field, value)
    
    await db.commit()
    await db.refresh(db_article)
    
    # 处理标签
    if article.tags is not None:
        await process_tags(db, "article", db_article.id, article.tags)
    
    return db_article

@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Article).where(Article.id == article_id)
    )
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    await db.delete(article)
    await db.commit()
    return {"message": "Article deleted successfully"}

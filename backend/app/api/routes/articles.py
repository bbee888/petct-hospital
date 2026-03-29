from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.article import Article, ArticleCategory
from app.schemas.article import ArticleCreate, ArticleUpdate, Article as ArticleSchema, ArticleCategoryCreate, ArticleCategoryUpdate, ArticleCategory as ArticleCategorySchema

router = APIRouter()

# 文章分类相关路由
@router.get("/categories", response_model=List[ArticleCategorySchema])
async def get_article_categories(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # domain = request.state.domain
    result = await db.execute(select(ArticleCategory).options(joinedload(ArticleCategory.articles)))
    categories = result.scalars().unique().all()
    return categories

@router.post("/categories", response_model=ArticleCategorySchema)
async def create_article_category(
    request: Request,
    category: ArticleCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain

    # 调试：打印接收到的数据
    print(f"接收到的文章分类数据: {category.model_dump()}")
    print(f"site_domain 值: {category.site_domain}")

    # 创建分类
    db_category = ArticleCategory(
        **category.model_dump()
    )
    print(f"创建的 db_category.site_domain: {db_category.site_domain}")
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
@router.get("/", response_model=List[ArticleSchema])
async def get_articles(
    request: Request,
    title: Optional[str] = None,
    site_domain: Optional[str] = None,
    category_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    # domain = request.state.domain
    query = select(Article).options(joinedload(Article.category))

    # 添加搜索条件
    if title:
        query = query.where(Article.title.contains(title))
    if site_domain:
        # 通过 category 关联查询 site_domain
        query = query.join(ArticleCategory).where(ArticleCategory.site_domain == site_domain)
    if category_id:
        query = query.where(Article.category_id == category_id)

    result = await db.execute(query)
    articles = result.scalars().unique().all()

    # 手动添加 site_domain 和 category_name
    result_list = []
    for article in articles:
        article_dict = {
            **ArticleSchema.model_validate(article).model_dump(),
            'site_domain': article.category.site_domain if article.category else None,
            'category_name': article.category.name if article.category else None
        }
        result_list.append(article_dict)

    return result_list

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

    # 调试：打印接收到的数据
    print(f"接收到的文章数据: {article.model_dump()}")

    # 创建文章 (site_domain 将从关联的 category 获取)
    db_article = Article(
        **article.model_dump()
    )
    print(f"创建的文章, 所属栏目 site_domain: {category.site_domain}")
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)

    return db_article

@router.get("/{article_id}", response_model=ArticleSchema)
async def get_article(
    article_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Article).options(joinedload(Article.category)).where(Article.id == article_id)
    )
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )

    # 更新浏览量：增加1-10的随机数
    import random
    view_increment = random.randint(1, 10)
    article.view_count = (article.view_count or 0) + view_increment
    await db.commit()

    # 添加 site_domain 和 category_name
    article_dict = {
        **ArticleSchema.model_validate(article).model_dump(),
        'site_domain': article.category.site_domain if article.category else None,
        'category_name': article.category.name if article.category else None
    }

    return article_dict

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
    for field, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, field, value)

    await db.commit()
    await db.refresh(db_article)

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

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.tag import Tag, article_tags, hospital_tags
from app.models.article import Article
from app.models.hospital import Hospital
from app.schemas.tag import Tag as TagSchema
from app.schemas.article import Article as ArticleSchema
from app.schemas.hospital import Hospital as HospitalSchema

router = APIRouter()

@router.get("/{slug}")
async def get_tag_aggregation(
    slug: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    domain = request.state.domain
    
    # 查询标签
    result = await db.execute(select(Tag).where(Tag.slug == slug))
    tag = result.scalars().first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    
    # 查询相关文章
    article_result = await db.execute(
        select(Article)
        .join(article_tags)
        .where(
            article_tags.c.tag_id == tag.id,
            Article.site_domain == domain,
            Article.is_published == True
        )
    )
    articles = article_result.scalars().all()
    
    # 查询相关医院
    hospital_result = await db.execute(
        select(Hospital)
        .join(hospital_tags)
        .where(
            hospital_tags.c.tag_id == tag.id,
            Hospital.site_domain == domain,
            Hospital.is_published == True
        )
    )
    hospitals = hospital_result.scalars().all()
    
    return {
        "tag": TagSchema.model_validate(tag),
        "articles": [ArticleSchema.model_validate(article) for article in articles],
        "hospitals": [HospitalSchema.model_validate(hospital) for hospital in hospitals]
    }

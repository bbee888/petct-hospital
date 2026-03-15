from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify
from app.models.tag import Tag, article_tags, hospital_tags
from app.models.article import Article
from app.models.hospital import Hospital

async def process_tags(db: AsyncSession, content_type: str, content_id: int, tag_string: str):
    # 分割标签并去重
    tags = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
    unique_tags = list(set(tags))
    
    # 收集标签 ID
    tag_ids = []
    for tag_name in unique_tags:
        # 生成 slug
        tag_slug = slugify(tag_name)
        
        # 查找或创建标签
        result = await db.execute(select(Tag).where(Tag.name == tag_name))
        tag = result.scalars().first()
        
        if not tag:
            # 创建新标签
            tag = Tag(name=tag_name, slug=tag_slug)
            db.add(tag)
            await db.commit()
            await db.refresh(tag)
        
        tag_ids.append(tag.id)
    
    # 删除旧关联
    if content_type == 'article':
        await db.execute(article_tags.delete().where(article_tags.c.article_id == content_id))
        # 批量插入新关联
        for tag_id in tag_ids:
            await db.execute(article_tags.insert().values(article_id=content_id, tag_id=tag_id))
    elif content_type == 'hospital':
        await db.execute(hospital_tags.delete().where(hospital_tags.c.hospital_id == content_id))
        # 批量插入新关联
        for tag_id in tag_ids:
            await db.execute(hospital_tags.insert().values(hospital_id=content_id, tag_id=tag_id))
    
    await db.commit()
    return tag_ids

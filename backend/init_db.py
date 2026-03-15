import asyncio
from app.db.session import engine
from app.db.base import Base

# 导入所有模型，确保它们被注册到Base.metadata
from app.models import User, Site, Hospital, Article, ArticleCategory, Appointment, Tag, Province, City, District

async def create_tables():
    async with engine.begin() as conn:
        # 先删除所有表
        await conn.run_sync(Base.metadata.drop_all)
        # 再创建所有表
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())

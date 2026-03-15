import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.geo import District
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def add_districts_table():
    # 创建数据库引擎
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # 创建 districts 表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, tables=[District.__table__])
    
    print("districts 表创建成功")
    
    # 关闭引擎
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(add_districts_table())

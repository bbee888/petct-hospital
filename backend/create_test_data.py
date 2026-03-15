import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.site import Site
from app.models.user import User
from app.models.geo import Province, City
from sqlalchemy import select
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_test_data():
    # 创建数据库引擎
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # 创建会话
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        # 创建测试站点
        result = await session.execute(select(Site).where(Site.domain == "petct.com"))
        existing_site = result.scalars().first()
        
        if not existing_site:
            test_site = Site(
                domain="petct.com",
                name="宠物CT中心",
                logo="https://example.com/logo.png",
                seo_keywords="宠物CT,宠物医疗,宠物检查",
                seo_description="专业的宠物CT检查中心，为您的宠物提供最优质的医疗服务",
                status=True
            )
            session.add(test_site)
            await session.commit()
            await session.refresh(test_site)
            print(f"测试站点创建成功: {test_site.name} ({test_site.domain})")
        else:
            print(f"测试站点已存在: {existing_site.name} ({existing_site.domain})")
        
        # 创建测试地理数据
        result = await session.execute(select(Province).where(Province.name == "广东省"))
        existing_province = result.scalars().first()
        
        if not existing_province:
            guangdong = Province(name="广东省")
            session.add(guangdong)
            await session.commit()
            await session.refresh(guangdong)
            
            guangzhou = City(province_id=guangdong.id, name="广州市")
            shenzhen = City(province_id=guangdong.id, name="深圳市")
            session.add_all([guangzhou, shenzhen])
            await session.commit()
            print("测试地理数据创建成功")
        else:
            print("测试地理数据已存在")
    
    # 关闭引擎
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_test_data())
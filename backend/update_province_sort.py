import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.session import async_session
from app.models.geo import Province

async def update_province_sort():
    async with async_session() as session:
        print("开始更新省份排序字段...")
        
        # 获取所有省份
        result = await session.execute(select(Province).order_by(Province.id))
        provinces = result.scalars().all()
        
        # 为每个省份设置sort值为其ID（默认排序）
        for province in provinces:
            if not province.sort or province.sort == 0:
                await session.execute(
                    update(Province).where(Province.id == province.id).values(sort=province.id)
                )
                print(f"省份 {province.name} (ID: {province.id}) 设置 sort = {province.id}")
        
        await session.commit()
        print("省份排序字段更新完成！")

if __name__ == "__main__":
    asyncio.run(update_province_sort())

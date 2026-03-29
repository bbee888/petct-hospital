"""
初始化医院合作标记数据
将所有现有医院的 is_cooperation 设置为 1（合作）
"""
import asyncio
from sqlalchemy import select, update
from app.db.session import get_db

async def init_cooperation_data():
    db = next(get_db())
    
    try:
        # 查询所有医院
        result = await db.execute(select(Hospital))
        hospitals = result.scalars().all()
        
        if not hospitals:
            print("没有找到医院数据")
            return
        
        print(f"找到 {len(hospitals)} 家医院")
        
        # 更新所有医院的 is_cooperation 为 1
        update_query = update(Hospital).values(is_cooperation=1)
        await db.execute(update_query)
        await db.commit()
        
        print(f"已将 {len(hospitals)} 家医院标记为合作医院")
        
    except Exception as e:
        await db.rollback()
        print(f"初始化失败：{str(e)}")
        raise
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(init_cooperation_data())

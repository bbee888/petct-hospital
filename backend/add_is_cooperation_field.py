"""
添加医院合作标记字段 is_cooperation
"""
import asyncio
from sqlalchemy import text
from app.db.session import get_db

async def migrate():
    db = next(get_db())
    
    try:
        # 检查字段是否已存在
        check_column_query = text("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'hospitals' 
            AND COLUMN_NAME = 'is_cooperation'
        """)
        
        result = await db.execute(check_column_query)
        count = result.scalar()
        
        if count > 0:
            print("字段 is_cooperation 已存在，无需添加")
            return
        
        # 添加 is_cooperation 字段
        add_column_query = text("""
            ALTER TABLE hospitals 
            ADD COLUMN is_cooperation INT DEFAULT 0 COMMENT '是否合作：0-未合作，1-合作'
        """)
        
        await db.execute(add_column_query)
        await db.commit()
        
        print("成功添加 is_cooperation 字段到 hospitals 表")
        
    except Exception as e:
        await db.rollback()
        print(f"迁移失败：{str(e)}")
        raise
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(migrate())

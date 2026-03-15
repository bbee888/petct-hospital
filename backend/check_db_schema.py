import asyncio
from sqlalchemy import text
from app.db.session import engine

async def check_db_schema():
    async with engine.begin() as conn:
        # 检查sites表的列
        result = await conn.execute(text("SHOW COLUMNS FROM sites"))
        columns = result.fetchall()
        print("sites表的列:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # 检查是否有seo_title列
        column_names = [col[0] for col in columns]
        if 'seo_title' not in column_names:
            print("\n缺少seo_title列，正在添加...")
            await conn.execute(text("ALTER TABLE sites ADD COLUMN seo_title VARCHAR(200) NULL AFTER logo"))
            print("seo_title列添加成功！")
        else:
            print("\nseo_title列已存在")

if __name__ == "__main__":
    asyncio.run(check_db_schema())

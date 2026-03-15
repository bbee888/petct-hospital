import asyncio
import aiomysql
from sqlalchemy import text
from app.db.session import engine

async def add_seo_title_column():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE sites ADD COLUMN seo_title VARCHAR(200) NULL AFTER logo"))
            print("成功添加 seo_title 字段到 sites 表")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("seo_title 字段已存在，跳过添加")
            else:
                print(f"添加字段失败: {e}")

if __name__ == "__main__":
    asyncio.run(add_seo_title_column())

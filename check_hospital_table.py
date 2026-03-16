import asyncio
import aiomysql
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check_hospital_table():
    DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/petct_manage_db"
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        result = await conn.execute(text("DESCRIBE hospitals"))
        columns = result.fetchall()
        print("Hospitals 表结构:")
        for column in columns:
            print(f"  {column}")

asyncio.run(check_hospital_table())

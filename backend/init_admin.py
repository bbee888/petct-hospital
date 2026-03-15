import asyncio
from app.db.session import async_session
from app.models.user import User
from app.core.security import get_password_hash

async def create_admin_user():
    async with async_session() as session:
        # 检查是否已存在admin用户
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.username == "admin"))
        existing_user = result.scalars().first()
        
        if existing_user:
            print("Admin user already exists!")
            return
        
        # 创建admin用户
        admin_user = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            email="admin@example.com",
            realname="系统管理员",
            is_active=True
        )
        session.add(admin_user)
        await session.commit()
        print("Admin user created successfully!")

if __name__ == "__main__":
    asyncio.run(create_admin_user())

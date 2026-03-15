import asyncio
import bcrypt
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.models.user import User
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def check_user():
    # 创建数据库引擎
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # 创建会话
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        # 查找admin用户
        result = await session.execute(select(User).where(User.username == "admin"))
        user = result.scalars().first()
        
        if user:
            print(f"找到用户: {user.username}")
            print(f"密码哈希: {user.password_hash}")
            print(f"用户状态: {'激活' if user.is_active else '未激活'}")
            
            # 测试密码验证
            test_password = "admin123"
            try:
                # 限制密码长度不超过72字节
                limited_password = test_password[:72].encode('utf-8')
                is_valid = bcrypt.checkpw(limited_password, user.password_hash.encode('utf-8'))
                print(f"密码验证结果: {'有效' if is_valid else '无效'}")
                
                # 如果验证失败，尝试用新的哈希方法生成密码并比较
                if not is_valid:
                    print("\n尝试生成新的密码哈希:")
                    new_hash = bcrypt.hashpw(limited_password, bcrypt.gensalt(12))
                    print(f"新哈希值: {new_hash.decode('utf-8')}")
                    print(f"与数据库哈希长度比较: {len(user.password_hash)} vs {len(new_hash.decode('utf-8'))}")
                    
                    # 尝试更新密码
                    user.password_hash = new_hash.decode('utf-8')
                    session.add(user)
                    await session.commit()
                    print("\n密码已更新为新的哈希格式")
                    
                    # 再次验证
                    is_valid_after_update = bcrypt.checkpw(limited_password, user.password_hash.encode('utf-8'))
                    print(f"更新后密码验证结果: {'有效' if is_valid_after_update else '无效'}")
                    
            except Exception as e:
                print(f"验证过程出错: {e}")
        else:
            print("未找到admin用户")
    
    # 关闭引擎
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_user())
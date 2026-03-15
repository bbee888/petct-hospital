import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "7"))

def verify_password(plain_password, hashed_password):
    """验证密码"""
    try:
        # 限制密码长度不超过72字节（bcrypt限制）
        limited_password = plain_password[:72].encode('utf-8')
        return bcrypt.checkpw(limited_password, hashed_password.encode('utf-8'))
    except Exception as e:
        print(f"密码验证错误: {e}")
        return False

def get_password_hash(password):
    """获取密码哈希值"""
    try:
        # 限制密码长度不超过72字节（bcrypt限制）
        limited_password = password[:72].encode('utf-8')
        hashed = bcrypt.hashpw(limited_password, bcrypt.gensalt(12))
        return hashed.decode('utf-8')
    except Exception as e:
        print(f"密码哈希错误: {e}")
        raise

def create_access_token(data: dict):
    """创建访问令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """解码令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
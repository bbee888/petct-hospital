from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.middleware.domain_middleware import domain_middleware
from app.db.base import Base
from app.db.session import engine
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源（如需要）

# 导入路由
from app.api.routes import auth, sites, hospitals, articles, appointments, tags, users, geo, categories, upload, stats

# 创建数据库表
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title="Hospital CMS API",
    description="多站点医院内容管理系统 API",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS - 必须在中间件之前
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://127.0.0.1:8080", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 注册域名中间件 - 放在 CORS 之后
app.middleware("http")(domain_middleware)

# 创建上传目录 - uploads目录在项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(sites.router, prefix="/api/v1/sites", tags=["sites"])
app.include_router(hospitals.router, prefix="/api/v1/hospitals", tags=["hospitals"])
app.include_router(articles.router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["appointments"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(geo.router, prefix="/api/v1/geo", tags=["geo"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["upload"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["stats"])


@app.get("/")
async def root():
    return {"message": "PETCT CMS API"}

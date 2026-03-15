from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.domain_middleware import domain_middleware
from app.db.base import Base
from app.db.session import engine

# 导入路由
from app.api.routes import auth, sites, hospitals, articles, appointments, tags, users, geo, categories, upload

# 创建数据库表
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(
    title="Hospital CMS API",
    description="多站点医院内容管理系统 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册域名中间件
app.middleware("http")(domain_middleware)

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

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Hospital CMS API"}

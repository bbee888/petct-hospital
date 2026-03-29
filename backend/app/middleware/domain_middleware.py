from fastapi import Request, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.models.site import Site
import os

SKIP_DOMAIN_CHECK_PATHS = [
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/v1/auth/login",
    "/api/v1/appointments",
    "/api/v1/hospitals",
    "/api/v1/articles",
    "/api/v1/geo"
]

async def domain_middleware(request: Request, call_next):
    path = request.url.path

    # 跳过所有API路径的域名检查（让CORS正常工作）
    if path.startswith("/api/"):
        response = await call_next(request)
        return response

    # 跳过 OPTIONS 预检请求
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response

    host = request.headers.get("host", "")
    if not host:
        raise HTTPException(status_code=404, detail="No host header provided")

    domain = host.split(":")[0]

    # 开发环境下，localhost 使用默认域名
    if domain in ["localhost", "127.0.0.1"]:
        request.state.domain = "localhost"
        response = await call_next(request)
        return response

    async with async_session() as session:
        result = await session.execute(
            select(Site).where(Site.domain == domain, Site.status == True)
        )
        site = result.scalars().first()

        if not site:
            raise HTTPException(status_code=404, detail="Site not found")

    request.state.domain = domain

    response = await call_next(request)
    return response

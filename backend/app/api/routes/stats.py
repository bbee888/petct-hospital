from fastapi import APIRouter, Depends
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.site import Site
from app.models.hospital import Hospital
from app.models.article import Article
from app.models.appointment import Appointment
from app.schemas.stats import StatsResponse, AppointmentStatsResponse, RecentAppointmentsResponse

router = APIRouter()

@router.get("/overview", response_model=StatsResponse)
async def get_stats_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取仪表盘统计数据
    包括: 站点数、医院数、文章数、预约数、用户数及其趋势
    """
    # 获取各表的总数
    sites_result = await db.execute(select(func.count(Site.id)))
    sites_count = sites_result.scalar() or 0
    
    hospitals_result = await db.execute(select(func.count(Hospital.id)))
    hospitals_count = hospitals_result.scalar() or 0
    
    articles_result = await db.execute(select(func.count(Article.id)))
    articles_count = articles_result.scalar() or 0
    
    appointments_result = await db.execute(select(func.count(Appointment.id)))
    appointments_count = appointments_result.scalar() or 0
    
    users_result = await db.execute(select(func.count(User.id)))
    users_count = users_result.scalar() or 0
    
    # TODO: 计算趋势数据 (环比上期)
    # 这里可以先返回None,后续可以添加日期范围查询来计算
    # 示例: 查询最近7天的数据与上一个7天比较
    
    return StatsResponse(
        sites_count=sites_count,
        hospitals_count=hospitals_count,
        articles_count=articles_count,
        appointments_count=appointments_count,
        users_count=users_count,
        sites_trend=5.2,  # 示例数据,后续需要真实计算
        hospitals_trend=12.8,
        articles_trend=8.5,
        appointments_trend=15.3,
        users_trend=3.2
    )

@router.get("/appointments/status", response_model=AppointmentStatsResponse)
async def get_appointments_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取预约状态统计
    包括: 待确认、已确认、已完成、已取消的数量
    """
    # 按状态统计预约数量
    # status: 0=pending, 1=confirmed, 2=completed, 3=cancelled
    
    pending_result = await db.execute(
        select(func.count(Appointment.id)).where(Appointment.status == 0)
    )
    pending_count = pending_result.scalar() or 0
    
    confirmed_result = await db.execute(
        select(func.count(Appointment.id)).where(Appointment.status == 1)
    )
    confirmed_count = confirmed_result.scalar() or 0
    
    completed_result = await db.execute(
        select(func.count(Appointment.id)).where(Appointment.status == 2)
    )
    completed_count = completed_result.scalar() or 0
    
    cancelled_result = await db.execute(
        select(func.count(Appointment.id)).where(Appointment.status == 3)
    )
    cancelled_count = cancelled_result.scalar() or 0
    
    return AppointmentStatsResponse(
        pending_count=pending_count,
        confirmed_count=confirmed_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count
    )

@router.get("/appointments/recent", response_model=RecentAppointmentsResponse)
async def get_recent_appointments(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取最近的预约记录
    默认返回最近10条
    """
    STATUS_MAP = {
        0: 'pending',
        1: 'confirmed',
        2: 'completed',
        3: 'cancelled'
    }
    
    from sqlalchemy.orm import selectinload
    
    result = await db.execute(
        select(Appointment)
        .options(selectinload(Appointment.hospital))
        .order_by(Appointment.created_at.desc())
        .limit(limit)
    )
    appointments = result.scalars().all()
    
    appointment_list = []
    for apt in appointments:
        appointment_list.append({
            'id': apt.id,
            'username': apt.username,
            'phone': apt.phone,
            'appoint_date': str(apt.appoint_date),
            'hospital_name': apt.hospital.title if apt.hospital else '未知医院',
            'status': STATUS_MAP.get(apt.status, 'pending')
        })
    
    return RecentAppointmentsResponse(
        appointments=appointment_list
    )

@router.get("/hospitals/cooperation")
async def get_cooperation_hospitals_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取合作医院数量统计
    """
    cooperation_result = await db.execute(
        select(func.count(Hospital.id)).where(Hospital.is_cooperation == 1)
    )
    cooperation_count = cooperation_result.scalar() or 0
    
    return {'cooperation_count': cooperation_count}

@router.get("/menu-badges")
async def get_menu_badges(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取菜单 badge 统计
    用于前端菜单显示的 badge 数字
    """
    # 站点数量
    sites_result = await db.execute(select(func.count(Site.id)))
    sites_badge = sites_result.scalar() or 0
    if sites_badge == 0:
        sites_badge = None
    
    # 医院数量
    hospitals_result = await db.execute(select(func.count(Hospital.id)))
    hospitals_badge = hospitals_result.scalar() or 0
    if hospitals_badge == 0:
        hospitals_badge = None
    
    # 文章数量
    articles_result = await db.execute(select(func.count(Article.id)))
    articles_badge = articles_result.scalar() or 0
    if articles_badge == 0:
        articles_badge = None
    
    # 预约数量
    appointments_result = await db.execute(select(func.count(Appointment.id)))
    appointments_badge = appointments_result.scalar() or 0
    if appointments_badge == 0:
        appointments_badge = None
    
    # 用户数量
    users_result = await db.execute(select(func.count(User.id)))
    users_badge = users_result.scalar() or 0
    if users_badge == 0:
        users_badge = None
    
    return {
        'sites': sites_badge,
        'hospitals': hospitals_badge,
        'articles': articles_badge,
        'appointments': appointments_badge,
        'users': users_badge
    }

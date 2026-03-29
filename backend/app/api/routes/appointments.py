from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.appointment import Appointment
from app.models.hospital import Hospital
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, Appointment as AppointmentSchema

router = APIRouter()

STATUS_MAP = {
    0: 'pending',
    1: 'confirmed',
    2: 'completed',
    3: 'cancelled'
}

STATUS_REVERSE_MAP = {v: k for k, v in STATUS_MAP.items()}

def format_appointment(apt, hospital_name=None):
    return {
        'id': apt.id,
        'site_domain': apt.site_domain,
        'hospital_id': apt.hospital_id,
        'hospital_name': hospital_name or (apt.hospital.name if apt.hospital else None),
        'username': apt.username,
        'phone': apt.phone,
        'idcard': apt.idcard,
        'sex': apt.sex,
        'appoint_date': apt.appoint_date,
        'intro': apt.intro,
        'created_at': apt.created_at,
        'status': STATUS_MAP.get(apt.status, 'pending')
    }

@router.get("/")
async def get_appointments(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Appointment).options(selectinload(Appointment.hospital)).order_by(Appointment.created_at.desc())
    )
    appointments = result.scalars().all()
    
    data = []
    for apt in appointments:
        data.append({
            'id': apt.id,
            'site_domain': apt.site_domain,
            'hospital_id': apt.hospital_id,
            'hospital_name': apt.hospital.title if apt.hospital else None,
            'username': apt.username,
            'phone': apt.phone,
            'idcard': apt.idcard,
            'sex': apt.sex,
            'appoint_date': str(apt.appoint_date),
            'intro': apt.intro,
            'created_at': str(apt.created_at),
            'status': STATUS_MAP.get(apt.status, 'pending')
        })
    return data

@router.post("/")
async def create_appointment(
    request: Request,
    appointment: AppointmentCreate,
    db: AsyncSession = Depends(get_db)
):
    domain = getattr(request.state, 'domain', None) or 'www.petctw.com'
    
    result = await db.execute(
        select(Hospital).where(Hospital.id == appointment.hospital_id)
    )
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital not found"
        )
    
    db_appointment = Appointment(
        hospital_id=appointment.hospital_id,
        username=appointment.username,
        phone=appointment.phone,
        idcard=appointment.idcard,
        sex=appointment.sex,
        appoint_date=appointment.appoint_date,
        intro=appointment.intro,
        site_domain=domain or '',
        status=0
    )
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    
    return {
        'id': db_appointment.id,
        'site_domain': db_appointment.site_domain,
        'hospital_id': db_appointment.hospital_id,
        'hospital_name': hospital.name,
        'username': db_appointment.username,
        'phone': db_appointment.phone,
        'idcard': db_appointment.idcard,
        'sex': db_appointment.sex,
        'appoint_date': str(db_appointment.appoint_date),
        'intro': db_appointment.intro,
        'created_at': str(db_appointment.created_at),
        'status': STATUS_MAP.get(db_appointment.status, 'pending')
    }

@router.get("/{appointment_id}")
async def get_appointment(
    appointment_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Appointment).options(selectinload(Appointment.hospital)).where(Appointment.id == appointment_id)
    )
    apt = result.scalars().first()
    if not apt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    return {
        'id': apt.id,
        'site_domain': apt.site_domain,
        'hospital_id': apt.hospital_id,
        'hospital_name': apt.hospital.title if apt.hospital else None,
        'username': apt.username,
        'phone': apt.phone,
        'idcard': apt.idcard,
        'sex': apt.sex,
        'appoint_date': str(apt.appoint_date),
        'intro': apt.intro,
        'created_at': str(apt.created_at),
        'status': STATUS_MAP.get(apt.status, 'pending')
    }

@router.put("/{appointment_id}")
async def update_appointment(
    appointment_id: int,
    request: Request,
    appointment: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Appointment).options(selectinload(Appointment.hospital)).where(Appointment.id == appointment_id)
    )
    db_appointment = result.scalars().first()
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    update_data = appointment.model_dump(exclude_unset=True)
    if 'status' in update_data and isinstance(update_data['status'], str):
        update_data['status'] = STATUS_REVERSE_MAP.get(update_data['status'], 0)
    
    for field, value in update_data.items():
        setattr(db_appointment, field, value)
    
    await db.commit()
    await db.refresh(db_appointment)
    
    return {
        'id': db_appointment.id,
        'site_domain': db_appointment.site_domain,
        'hospital_id': db_appointment.hospital_id,
        'hospital_name': db_appointment.hospital.title if db_appointment.hospital else None,
        'username': db_appointment.username,
        'phone': db_appointment.phone,
        'idcard': db_appointment.idcard,
        'sex': db_appointment.sex,
        'appoint_date': str(db_appointment.appoint_date),
        'intro': db_appointment.intro,
        'created_at': str(db_appointment.created_at),
        'status': STATUS_MAP.get(db_appointment.status, 'pending')
    }

@router.delete("/{appointment_id}")
async def delete_appointment(
    appointment_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # domain = request.state.domain
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id)
    )
    appointment = result.scalars().first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    await db.delete(appointment)
    await db.commit()
    return {"message": "Appointment deleted successfully"}

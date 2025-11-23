from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List
from app.db.session import get_db
from app.models.appointment import Appointment
from app.models.pet import Pet
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter()

@router.post("/", response_model=AppointmentResponse)
async def create_appointment(
    appointment: AppointmentCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Verify Pet Exists
    pet = await db.get(Pet, appointment.pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # 2. Verify Doctor Exists
    doctor = await db.get(Doctor, appointment.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # 3. Create Appointment
    new_appointment = Appointment(
        pet_id=appointment.pet_id,
        doctor_id=appointment.doctor_id,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        reason=appointment.reason,
        notes=appointment.notes,
        # status defaults to 'scheduled' via the Model
    )

    try:
        db.add(new_appointment)
        await db.commit()
        await db.refresh(new_appointment)
        return new_appointment
        
    except IntegrityError:
        # This catches DB-level constraint errors (like foreign key failures)
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint failed.")
    
    
@router.get("/", response_model=List[AppointmentResponse])
async def get_appointments(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    # Simple select all
    result = await db.execute(select(Appointment).offset(skip).limit(limit))
    return result.scalars().all()

# --- READ ONE (GET) ---
@router.get("/{id}", response_model=AppointmentResponse)
async def get_appointment(id: int, db: AsyncSession = Depends(get_db)):
    # Fetch by ID
    result = await db.execute(select(Appointment).where(Appointment.id == id))
    appointment = result.scalars().first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    return appointment
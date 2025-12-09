# # from fastapi import APIRouter, Depends, HTTPException
# # from sqlalchemy.ext.asyncio import AsyncSession
# # from sqlalchemy.future import select
# # from sqlalchemy.exc import IntegrityError
# # from typing import List
# # from app.db.session import get_db
# # from app.models.appointment import Appointment
# # from app.models.pet import Pet
# # from app.models.doctor import Doctor
# # from app.schemas.appointment import AppointmentCreate, AppointmentResponse

# # router = APIRouter()

# # @router.post("/", response_model=AppointmentResponse)
# # async def create_appointment(
# #     appointment: AppointmentCreate, 
# #     db: AsyncSession = Depends(get_db)
# # ):
# #     # 1. Verify Pet Exists
# #     pet = await db.get(Pet, appointment.pet_id)
# #     if not pet:
# #         raise HTTPException(status_code=404, detail="Pet not found")

# #     # 2. Verify Doctor Exists
# #     doctor = await db.get(Doctor, appointment.doctor_id)
# #     if not doctor:
# #         raise HTTPException(status_code=404, detail="Doctor not found")

# #     # 3. Create Appointment
# #     new_appointment = Appointment(
# #         pet_id=appointment.pet_id,
# #         doctor_id=appointment.doctor_id,
# #         start_time=appointment.start_time,
# #         end_time=appointment.end_time,
# #         reason=appointment.reason,
# #         notes=appointment.notes,
# #         # status defaults to 'scheduled' via the Model
# #     )

# #     try:
# #         db.add(new_appointment)
# #         await db.commit()
# #         await db.refresh(new_appointment)
# #         return new_appointment
        
# #     except IntegrityError:
# #         # This catches DB-level constraint errors (like foreign key failures)
# #         await db.rollback()
# #         raise HTTPException(status_code=400, detail="Database constraint failed.")
    
    
# # @router.get("/", response_model=List[AppointmentResponse])
# # async def get_appointments(
# #     skip: int = 0, 
# #     limit: int = 100, 
# #     db: AsyncSession = Depends(get_db)
# # ):
# #     # Simple select all
# #     result = await db.execute(select(Appointment).offset(skip).limit(limit))
# #     return result.scalars().all()

# # # --- READ ONE (GET) ---
# # @router.get("/{id}", response_model=AppointmentResponse)
# # async def get_appointment(id: int, db: AsyncSession = Depends(get_db)):
# #     # Fetch by ID
# #     result = await db.execute(select(Appointment).where(Appointment.id == id))
# #     appointment = result.scalars().first()
    
# #     if not appointment:
# #         raise HTTPException(status_code=404, detail="Appointment not found")
        
# #     return appointment



# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import selectinload
# from typing import List, Optional
# from app.db.session import get_db
# from app.models.appointment import Appointment
# from app.models.pet import Pet
# from app.models.doctor import Doctor
# from app.schemas.appointment import AppointmentCreate, AppointmentResponse

# router = APIRouter()

# # --- CREATE APPOINTMENT ---
# @router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
# async def create_appointment(
#     appointment: AppointmentCreate, 
#     db: AsyncSession = Depends(get_db)
# ):
#     # 1. Verify Pet Exists
#     pet = await db.get(Pet, appointment.pet_id)
#     if not pet:
#         raise HTTPException(status_code=404, detail="Pet not found")

#     # 2. Verify Doctor Exists (Optional logic check)
#     # Note: If your doctor_id is optional in DB, handle that here. Assuming required:
#     doctor = await db.get(Doctor, appointment.doctor_id)
#     if not doctor:
#         raise HTTPException(status_code=404, detail="Doctor not found")

#     # 3. Create Appointment
#     new_appointment = Appointment(
#         pet_id=appointment.pet_id,
#         doctor_id=appointment.doctor_id,
#         start_time=appointment.start_time,
#         end_time=appointment.end_time,
#         reason=appointment.reason,
#         notes=appointment.notes,
#         status="scheduled" # Default status
#     )

#     try:
#         db.add(new_appointment)
#         await db.commit()
#         await db.refresh(new_appointment)
#         return new_appointment
        
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=400, detail="Database constraint failed.")

# # --- GET ALL (With Optional Filtering) ---
# @router.get("/", response_model=List[AppointmentResponse])
# async def get_appointments(
#     skip: int = 0, 
#     limit: int = 100, 
#     pet_id: Optional[int] = None, # Added optional filter
#     db: AsyncSession = Depends(get_db)
# ):
#     query = select(Appointment).offset(skip).limit(limit)
    
#     # If frontend sends ?pet_id=5, we only return those appointments
#     if pet_id:
#         query = query.where(Appointment.pet_id == pet_id)
    
#     # Execute
#     result = await db.execute(query)
#     return result.scalars().all()

# # --- GET ONE ---
# @router.get("/{id}", response_model=AppointmentResponse)
# async def get_appointment(id: int, db: AsyncSession = Depends(get_db)):
#     # Fetch by ID
#     result = await db.execute(select(Appointment).where(Appointment.id == id))
#     appointment = result.scalars().first()
    
#     if not appointment:
#         raise HTTPException(status_code=404, detail="Appointment not found")
        
#     return appointment



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from pydantic import BaseModel # <--- ADDED THIS IMPORT

from app.db.session import get_db
from app.models.appointment import Appointment
from app.models.pet import Pet
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter()

# --- INLINE SCHEMA FOR STATUS UPDATES ---
class AppointmentUpdate(BaseModel):
    status: str

# --- CREATE APPOINTMENT ---
@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
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
        status="scheduled" # Default status
    )

    try:
        db.add(new_appointment)
        await db.commit()
        await db.refresh(new_appointment)
        return new_appointment
        
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Database constraint failed.")

# --- GET ALL (With Optional Filtering) ---
@router.get("/", response_model=List[AppointmentResponse])
async def get_appointments(
    skip: int = 0, 
    limit: int = 100, 
    pet_id: Optional[int] = None, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Appointment).offset(skip).limit(limit)
    
    # If frontend sends ?pet_id=5, we only return those appointments
    if pet_id:
        query = query.where(Appointment.pet_id == pet_id)
    
    # Execute
    result = await db.execute(query)
    return result.scalars().all()

# --- GET ONE ---
@router.get("/{id}", response_model=AppointmentResponse)
async def get_appointment(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment).where(Appointment.id == id))
    appointment = result.scalars().first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
        
    return appointment

# --- NEW: UPDATE STATUS (For Billing) ---
@router.put("/{id}", response_model=AppointmentResponse)
async def update_appointment_status(
    id: int, 
    status_update: AppointmentUpdate, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Fetch the appointment
    result = await db.execute(select(Appointment).where(Appointment.id == id))
    appointment = result.scalars().first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # 2. Update the status
    appointment.status = status_update.status
    
    # 3. Save
    await db.commit()
    await db.refresh(appointment)
    return appointment
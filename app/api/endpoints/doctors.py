# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# from app.db.session import get_db
# from app.models.doctor import Doctor
# from app.schemas.doctor import DoctorCreate, DoctorResponse

# router = APIRouter()

# @router.post("/", response_model=DoctorResponse)
# async def create_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
#     new_doctor = Doctor(**doctor.model_dump())
#     db.add(new_doctor)
#     await db.commit()
#     await db.refresh(new_doctor)
    
#     return new_doctor

# @router.get("/", response_model=list[DoctorResponse])
# async def get_doctors(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Doctor))
#     return result.scalars().all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from app.db.session import get_db
from app.models.doctor import Doctor

router = APIRouter()

# --- SCHEMAS ---
class DoctorResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    specialization: str
    
    # FIX: Make these optional to prevent crashes on old data
    email: Optional[str] = None
    contact_number: Optional[str] = None
    
    is_active: bool

    class Config:
        from_attributes = True

# ... (Keep the rest of the file exactly as it was) ...

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    email: str
    contact_number: str
    is_active: bool = True

class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[str] = None
    contact_number: Optional[str] = None
    is_active: Optional[bool] = None

# --- ENDPOINTS ---

@router.get("/", response_model=List[DoctorResponse])
async def get_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor))
    return result.scalars().all()

@router.post("/", response_model=DoctorResponse)
async def create_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    new_doc = Doctor(
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        specialization=doctor.specialization,
        email=doctor.email,
        contact_number=doctor.contact_number,
        is_active=doctor.is_active
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return new_doc

@router.put("/{id}", response_model=DoctorResponse)
async def update_doctor(id: int, doctor_update: DoctorUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).where(Doctor.id == id))
    doctor = result.scalars().first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    update_data = doctor_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(doctor, key, value)

    await db.commit()
    await db.refresh(doctor)
    return doctor
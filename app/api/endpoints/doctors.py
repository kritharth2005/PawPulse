from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter()

@router.post("/", response_model=DoctorResponse)
async def create_doctor(doctor: DoctorCreate, db: AsyncSession = Depends(get_db)):
    new_doctor = Doctor(**doctor.model_dump())
    db.add(new_doctor)
    await db.commit()
    await db.refresh(new_doctor)
    
    return new_doctor

@router.get("/", response_model=list[DoctorResponse])
async def get_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor))
    return result.scalars().all()
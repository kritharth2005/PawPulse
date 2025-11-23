from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.medical_record import MedicalRecord
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse

router = APIRouter()

@router.post("/", response_model=MedicalRecordResponse)
async def create_medical_record(
    record: MedicalRecordCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Fetch the Appointment
    appointment = await db.get(Appointment, record.appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # 2. Check if a record already exists (Prevent duplicates)
    # Since we set unique=True in DB, this is a double-check for better error messages
    existing_record = await db.execute(
        select(MedicalRecord).where(MedicalRecord.appointment_id == record.appointment_id)
    )
    if existing_record.scalars().first():
        raise HTTPException(status_code=400, detail="Medical Record already exists for this appointment")

    # 3. Create the Record
    new_record = MedicalRecord(**record.model_dump())
    db.add(new_record)
    
    # 4. AUTOMATION: Update Appointment Status to COMPLETED
    appointment.status = AppointmentStatus.COMPLETED
    db.add(appointment) # Add to session to be updated

    # 5. Commit Transaction (Atomic: Record created + Status updated)
    await db.commit()
    await db.refresh(new_record)
    
    return new_record
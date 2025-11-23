from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class MedicalRecordBase(BaseModel):
    appointment_id: int
    diagnosis: str
    treatment: str
    pet_weight: float
    next_visit_date: Optional[date] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
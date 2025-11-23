from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
from app.models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    pet_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    reason: str
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    # Senior Dev Tip: Validate logic in the schema before it hits the DB
    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

class AppointmentResponse(AppointmentBase):
    id: int
    status: AppointmentStatus
    created_at: datetime

    class Config:
        from_attributes = True
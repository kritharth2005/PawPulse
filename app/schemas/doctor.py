from pydantic import BaseModel
from datetime import datetime

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
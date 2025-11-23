from pydantic import BaseModel

class PrescriptionCreate(BaseModel):
    medical_record_id: int
    inventory_id: int
    quantity: int
    instructions: str

class PrescriptionResponse(PrescriptionCreate):
    id: int

    class Config:
        from_attributes = True
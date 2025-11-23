from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.pet import AnimalType

class PetBase(BaseModel):
    name: str
    age: Optional[int] = None
    animal_type: AnimalType

class PetCreate(PetBase):
    owner_id: int

class PetCreateNested(PetBase):
    pass

class PetResponse(PetBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
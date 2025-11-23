from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from app.schemas.pet import PetCreateNested, PetResponse

# 1. Shared properties (used for creating AND reading)
class OwnerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    contact_number: str
    address: Optional[str] = None

# 2. Properties to receive on creation (What the frontend sends)
class OwnerCreate(OwnerBase):
    pets: List[PetCreateNested] = []

# 3. Properties to return to client (What the API sends back)
class OwnerResponse(OwnerBase):
    id: int
    created_at: datetime
    pets: List[PetResponse] = []
    # We exclude updated_at to keep the response clean, unless you want it.

    class Config:
        from_attributes = True
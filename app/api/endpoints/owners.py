# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.orm import selectinload
# from app.db.session import get_db
# from app.models.owner import Owner
# from app.models.pet import Pet
# from app.schemas.owner import OwnerCreate, OwnerResponse

# router = APIRouter()

# @router.post("/", response_model=OwnerResponse)
# async def create_owner(owner: OwnerCreate, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Owner).where(Owner.email == owner.email))
#     if result.scalars().first():
#         raise HTTPException(status_code=400, detail="Email already registered")
#     owner_data = owner.model_dump(exclude={"pets"})
#     new_owner = Owner(**owner_data)
    
#     if owner.pets:
#         for pet_data in owner.pets:
#             new_pet = Pet(
#                 **pet_data.model_dump()
#             )
#             new_owner.pets.append(new_pet)  
            
#     db.add(new_owner)
#     await db.commit()
    
#     stmt = (
#         select(Owner)
#         .options(selectinload(Owner.pets))
#         .where(Owner.id == new_owner.id)
#     )
    
#     result = await db.execute(stmt)
#     new_owner = result.scalars().first()
    
#     return new_owner




from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List 

from app.db.session import get_db
from app.models.owner import Owner
from app.models.pet import Pet
from app.schemas.owner import OwnerCreate, OwnerResponse

router = APIRouter()

# --- 1. CREATE OWNER (Already existed) ---
@router.post("/", response_model=OwnerResponse)
async def create_owner(owner: OwnerCreate, db: AsyncSession = Depends(get_db)):
    # Check uniqueness
    result = await db.execute(select(Owner).where(Owner.email == owner.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create Owner
    owner_data = owner.model_dump(exclude={"pets"}) 
    new_owner = Owner(**owner_data)
    
    # Create Pets
    if owner.pets:
        for pet_data in owner.pets:
            new_pet = Pet(**pet_data.model_dump())
            new_owner.pets.append(new_pet)

    db.add(new_owner)
    await db.commit()
    
    # Reload with pets for the response
    stmt = (
        select(Owner)
        .options(selectinload(Owner.pets))
        .where(Owner.id == new_owner.id)
    )
    result = await db.execute(stmt)
    new_owner = result.scalars().first()
    
    return new_owner

# --- 2. GET ALL OWNERS (The Missing Piece!) ---
@router.get("/", response_model=List[OwnerResponse])
async def get_owners(db: AsyncSession = Depends(get_db)):
    # We use selectinload to fetch the pets along with the owner
    # otherwise 'pets' array will be empty in the frontend
    stmt = select(Owner).options(selectinload(Owner.pets))
    result = await db.execute(stmt)
    return result.scalars().all()
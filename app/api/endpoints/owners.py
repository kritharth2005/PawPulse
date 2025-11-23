from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.models.owner import Owner
from app.models.pet import Pet
from app.schemas.owner import OwnerCreate, OwnerResponse

router = APIRouter()

@router.post("/", response_model=OwnerResponse)
async def create_owner(owner: OwnerCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Owner).where(Owner.email == owner.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    owner_data = owner.model_dump(exclude={"pets"})
    new_owner = Owner(**owner_data)
    
    if owner.pets:
        for pet_data in owner.pets:
            new_pet = Pet(
                **pet_data.model_dump()
            )
            new_owner.pets.append(new_pet)  
            
    db.add(new_owner)
    await db.commit()
    
    stmt = (
        select(Owner)
        .options(selectinload(Owner.pets))
        .where(Owner.id == new_owner.id)
    )
    
    result = await db.execute(stmt)
    new_owner = result.scalars().first()
    
    return new_owner
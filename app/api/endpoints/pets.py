from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetResponse
from app.models.owner import Owner

router = APIRouter()

@router.post("/", response_model=PetResponse)
async def create_pet(pet: PetCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Owner).where(Owner.id == pet.owner_id))
    owner = result.scalars().first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    new_pet = Pet(
        name=pet.name,
        age=pet.age,
        animal_type=pet.animal_type,
        owner_id=pet.owner_id
    )
    
    db.add(new_pet)
    await db.commit()
    await db.refresh(new_pet)
    
    return new_pet
    
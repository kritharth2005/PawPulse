from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryResponse

router = APIRouter()

@router.post("/", response_model=InventoryResponse)
async def create_item(item: InventoryCreate, db: AsyncSession = Depends(get_db)):
    new_item = Inventory(**item.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[InventoryResponse])
async def get_inventory(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Inventory))
    return result.scalars().all()
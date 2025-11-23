from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.prescription import Prescription
from app.models.inventory import Inventory
from app.models.medical_record import MedicalRecord
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse

router = APIRouter()

@router.post("/", response_model=PrescriptionResponse)
async def create_prescription(
    prescription: PrescriptionCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 1. Verify Medical Record Exists
    record = await db.get(MedicalRecord, prescription.medical_record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Medical Record not found")

    # 2. Fetch Inventory Item
    item = await db.get(Inventory, prescription.inventory_id)
    if not item:
        raise HTTPException(status_code=404, detail="Medicine not found in inventory")

    # 3. STOCK CHECK (Business Logic)
    if item.stock < prescription.quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough stock. Available: {item.stock}"
        )

    # 4. DECREMENT STOCK
    item.stock -= prescription.quantity
    
    # 5. Create Prescription
    new_prescription = Prescription(**prescription.model_dump())
    
    # 6. Atomic Commit (Save Prescription AND Update Stock)
    db.add(item)
    db.add(new_prescription)
    
    await db.commit()
    await db.refresh(new_prescription)
    
    return new_prescription
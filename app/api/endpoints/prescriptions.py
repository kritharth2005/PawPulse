# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.db.session import get_db
# from app.models.prescription import Prescription
# from app.models.inventory import Inventory
# from app.models.medical_record import MedicalRecord
# from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse

# router = APIRouter()

# @router.post("/", response_model=PrescriptionResponse)
# async def create_prescription(
#     prescription: PrescriptionCreate, 
#     db: AsyncSession = Depends(get_db)
# ):
#     # 1. Verify Medical Record Exists
#     record = await db.get(MedicalRecord, prescription.medical_record_id)
#     if not record:
#         raise HTTPException(status_code=404, detail="Medical Record not found")

#     # 2. Fetch Inventory Item
#     item = await db.get(Inventory, prescription.inventory_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Medicine not found in inventory")

#     # 3. STOCK CHECK (Business Logic)
#     if item.stock < prescription.quantity:
#         raise HTTPException(
#             status_code=400, 
#             detail=f"Not enough stock. Available: {item.stock}"
#         )

#     # 4. DECREMENT STOCK
#     item.stock -= prescription.quantity
    
#     # 5. Create Prescription
#     new_prescription = Prescription(**prescription.model_dump())
    
#     # 6. Atomic Commit (Save Prescription AND Update Stock)
#     db.add(item)
#     db.add(new_prescription)
    
#     await db.commit()
#     await db.refresh(new_prescription)
    
#     return new_prescription


# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from app.db.session import get_db
# from app.models.inventory import Inventory  # Importing your model
# from app.models.appointment import Appointment
# from pydantic import BaseModel
# from typing import List, Optional

# router = APIRouter()

# # --- SCHEMAS (Data Validation) ---
# class PrescriptionItemCreate(BaseModel):
#     inventory_id: int
#     quantity: int
#     dosage: str  # e.g., "1 tablet twice daily"

# class PrescriptionCreate(BaseModel):
#     appointment_id: int
#     notes: Optional[str] = None
#     items: List[PrescriptionItemCreate]

# # --- ENDPOINT ---
# @router.post("/")
# async def create_prescription(
#     data: PrescriptionCreate, 
#     db: AsyncSession = Depends(get_db)
# ):
#     # 1. Verify Appointment Exists
#     apt_result = await db.execute(select(Appointment).where(Appointment.id == data.appointment_id))
#     appointment = apt_result.scalars().first()
    
#     if not appointment:
#         raise HTTPException(status_code=404, detail="Appointment not found")

#     # 2. Process Items (Check Stock & Deduct)
#     summary_text = [] 
    
#     for item in data.items:
#         # Fetch Inventory Item
#         inv_result = await db.execute(select(Inventory).where(Inventory.id == item.inventory_id))
#         inventory_item = inv_result.scalars().first()

#         if not inventory_item:
#             raise HTTPException(status_code=404, detail=f"Item ID {item.inventory_id} not found")

#         # Check Stock (Using your model's 'stock' column)
#         if inventory_item.stock < item.quantity:
#             raise HTTPException(
#                 status_code=400, 
#                 detail=f"Not enough stock for '{inventory_item.name}'. Available: {inventory_item.stock}"
#             )

#         # --- DEDUCT INVENTORY ---
#         inventory_item.stock -= item.quantity
#         db.add(inventory_item) 
        
#         summary_text.append(f"- {inventory_item.name} (Qty: {item.quantity}) | {item.dosage}")

#     # 3. Save Record to Appointment Notes
#     new_note = "\n--- PRESCRIPTION ---\n" + "\n".join(summary_text)
    
#     if data.notes:
#         new_note += f"\nNote: {data.notes}"

#     if appointment.notes:
#         appointment.notes += "\n" + new_note
#     else:
#         appointment.notes = new_note

#     # 4. Commit All Changes
#     try:
#         await db.commit()
#     except Exception as e:
#         await db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

#     return {"status": "success", "message": "Prescription created and stock updated."}




from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.inventory import Inventory
from app.models.appointment import Appointment
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# --- SCHEMAS ---
class PrescriptionItemCreate(BaseModel):
    inventory_id: int
    quantity: int
    dosage: str

class PrescriptionCreate(BaseModel):
    appointment_id: int
    notes: Optional[str] = None
    items: List[PrescriptionItemCreate]

# --- ENDPOINT ---
@router.post("/")
async def create_prescription(
    data: PrescriptionCreate, 
    db: AsyncSession = Depends(get_db)
):
    # 0. Validate Duplicates (Input Side)
    item_ids = [item.inventory_id for item in data.items]
    if len(item_ids) != len(set(item_ids)):
        raise HTTPException(status_code=400, detail="Duplicate medicines selected. Please combine quantities.")

    # 1. Verify Appointment Exists
    apt_result = await db.execute(select(Appointment).where(Appointment.id == data.appointment_id))
    appointment = apt_result.scalars().first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # 2. Process Items (Check Stock, Deduct, Calculate Bill)
    summary_text = []
    total_cost = 0.0
    
    for item in data.items:
        # Fetch Inventory Item
        inv_result = await db.execute(select(Inventory).where(Inventory.id == item.inventory_id))
        inventory_item = inv_result.scalars().first()

        if not inventory_item:
            raise HTTPException(status_code=404, detail=f"Item ID {item.inventory_id} not found")

        # Check Stock
        if inventory_item.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock for '{inventory_item.name}'. Available: {inventory_item.stock}"
            )

        # --- DEDUCT INVENTORY ---
        inventory_item.stock -= item.quantity
        db.add(inventory_item) 
        
        # --- CALCULATE COST ---
        item_total = inventory_item.price * item.quantity
        total_cost += item_total

        # Format: Name (Qty) - Dosage | $Cost
        summary_text.append(f"- {inventory_item.name} (Qty: {item.quantity}) | {item.dosage} | ₹{item_total}")

    # 3. Save Record to Appointment Notes
    new_note = "\n--- PRESCRIPTION ---\n" + "\n".join(summary_text)
    new_note += f"\n\nTotal Medicine Cost: ₹{total_cost}"
    
    if data.notes:
        new_note += f"\nNote: {data.notes}"

    if appointment.notes:
        appointment.notes += "\n" + new_note
    else:
        appointment.notes = new_note

    # 4. Commit All Changes
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "message": f"Prescription created. Total Cost: ₹{total_cost}"}
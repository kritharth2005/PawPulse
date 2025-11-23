from pydantic import BaseModel

class InventoryBase(BaseModel):
    name: str
    stock: int
    price: float

class InventoryCreate(InventoryBase):
    pass

class InventoryResponse(InventoryBase):
    id: int

    class Config:
        from_attributes = True
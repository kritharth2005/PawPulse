from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False) # e.g. "Amoxicillin 500mg"
    stock = Column(Integer, default=0) # How many items we have
    price = Column(Float, nullable=False) # Cost per unit

    # Relationship (One inventory item can be in many prescriptions)
    prescriptions = relationship("Prescription", back_populates="inventory_item")
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    
    # Links
    medical_record_id = Column(Integer, ForeignKey("medical_records.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    
    quantity = Column(Integer, default=1) # How many pills/bottles?
    instructions = Column(String, nullable=True) # e.g. "Twice a day after food"

    # Relationships
    medical_record = relationship("MedicalRecord", backref="prescriptions")
    inventory_item = relationship("Inventory", back_populates="prescriptions")
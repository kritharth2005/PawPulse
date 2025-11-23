from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    specialization = Column(String(100), nullable=False) # e.g., "Surgeon", "Dermatologist"
    is_active = Column(Boolean, default=True) # Soft delete mechanism

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to Appointments (We will create this next)
    appointments = relationship("Appointment", back_populates="doctor")
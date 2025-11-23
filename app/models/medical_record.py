from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    
    # One-to-One: Linking to a specific appointment
    # unique=True ensures one appointment cannot have two different records
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=False)
    
    diagnosis = Column(String(255), nullable=False) # e.g. "Ear Infection"
    treatment = Column(String, nullable=False)      # e.g. "Cleaned ears, applied drops"
    pet_weight = Column(Float, nullable=True)       # e.g. 12.5 (kg)
    
    # Optional: Doctor suggests next visit
    next_visit_date = Column(Date, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    appointment = relationship("Appointment", back_populates="medical_record")
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class AppointmentStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    
    # Details
    reason = Column(String(255), nullable=False) # e.g., "Annual Vaccination"
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.SCHEDULED)
    notes = Column(String, nullable=True) # Doctor's notes after visit

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    pet = relationship("Pet", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    medical_record = relationship("MedicalRecord", back_populates="appointment", uselist=False)
    
    # DBMS BONUS: Table Args for Database-Level Constraints
    __table_args__ = (
        # Ensure End Time is ALWAYS greater than Start Time
        CheckConstraint('end_time > start_time', name='check_end_time_after_start'),
    )
    
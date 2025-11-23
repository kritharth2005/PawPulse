from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

# Define strict choices for animal types
class AnimalType(str, enum.Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    OTHER = "other"

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=True)
    
    # The Enum restricts this column to only specific values
    animal_type = Column(SQLEnum(AnimalType), nullable=False)
    
    # FOREIGN KEY: This links the Pet to the Owner table
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (Allows us to do pet.owner or owner.pets)
    # Note: We need to update the Owner model to match this 'back_populates'
    owner = relationship("Owner", back_populates="pets")
    appointments = relationship("Appointment", back_populates="pet")
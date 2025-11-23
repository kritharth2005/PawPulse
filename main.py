from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import owners, pets, doctors, appointments, medical_records, inventory, prescriptions
from fastapi.middleware.cors import CORSMiddleware
from app import models

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(owners.router, prefix="/owners", tags=["Owners"])
app.include_router(pets.router, prefix="/pets", tags=["Pets"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(medical_records.router, prefix="/medical-records", tags=["Medical Records"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])

@app.get("/")
async def root():
    return {"message": "Welcome to PawPulse API!", "status": "running"}
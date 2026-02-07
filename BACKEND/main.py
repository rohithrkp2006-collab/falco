from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

hospitals = []
patients = []
consents = []

@app.get("/")
def root():
    return {"status": "Backend is running (VS Code)"}

class Hospital(BaseModel):
    name: str
    license_no: str

@app.post("/hospital/register")
def register_hospital(h: Hospital):
    hospitals.append(h)
    return {"message": "Hospital registered"}

class Patient(BaseModel):
    phone: str

@app.post("/patient/register")
def register_patient(p: Patient):
    patients.append(p)
    return {"message": "Patient registered"}

class Consent(BaseModel):
    patient_phone: str
    hospital_name: str

@app.post("/consent/approve")
def approve_consent(c: Consent):
    expiry = datetime.utcnow() + timedelta(hours=6)
    consents.append({
        "patient": c.patient_phone,
        "hospital": c.hospital_name,
        "expiry": expiry
    })
    return {"message": "Consent approved for 6 hours"}

@app.get("/records")
def get_records(patient_phone: str, hospital_name: str):
    for c in consents:
        if c["patient"] == patient_phone and c["hospital"] == hospital_name and c["expiry"] > datetime.utcnow():
            return {"records": ["Blood Test", "X-Ray", "Prescription"]}
    return {"error": "No active consent"}

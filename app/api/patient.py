from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.services.patient_service import create_patient, get_patient, update_patient

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", response_model=PatientRead)
async def create_patient_endpoint(
    payload: PatientCreate,
    db: AsyncSession = Depends(get_db_session),
):
    return await create_patient(db, payload)


@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient_endpoint(patient_id: str, db: AsyncSession = Depends(get_db_session)):
    patient = await get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.patch("/{patient_id}", response_model=PatientRead)
async def update_patient_endpoint(
    patient_id: str,
    payload: PatientUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    patient = await get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return await update_patient(db, patient, payload)


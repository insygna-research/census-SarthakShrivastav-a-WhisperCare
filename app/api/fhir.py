from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.intake import IntakeSession
from app.services.fhir_service import build_patient_bundle
from app.services.patient_service import get_patient

router = APIRouter(prefix="/abdm", tags=["abdm"])


@router.get("/export/{patient_id}")
async def export_patient_bundle(patient_id: str, db: AsyncSession = Depends(get_db_session)):
    patient = await get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    result = await db.execute(select(IntakeSession).where(IntakeSession.patient_id == patient_id))
    return build_patient_bundle(patient, list(result.scalars().all()))


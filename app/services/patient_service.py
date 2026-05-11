from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.services.audit_service import record_audit_event


async def create_patient(db: AsyncSession, payload: PatientCreate) -> Patient:
    settings = get_settings()
    patient = Patient(
        phone=payload.phone,
        full_name=payload.full_name,
        age=payload.age,
        gender=payload.gender,
        state=payload.state or settings.india.default_state,
        preferred_language=payload.preferred_language or settings.languages.default,
        emergency_contact=payload.emergency_contact,
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    await record_audit_event(
        db,
        event_type="patient.created",
        entity_type="patient",
        entity_id=patient.id,
        actor_id=patient.id,
        actor_type="patient",
    )
    return patient


async def get_patient(db: AsyncSession, patient_id: str) -> Patient | None:
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    return result.scalar_one_or_none()


async def update_patient(db: AsyncSession, patient: Patient, payload: PatientUpdate) -> Patient:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)
    await db.commit()
    await db.refresh(patient)
    return patient


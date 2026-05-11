from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.consent import PatientConsent
from app.schemas.consent import ConsentCreate
from app.services.audit_service import record_audit_event


async def create_consent(db: AsyncSession, payload: ConsentCreate) -> PatientConsent:
    consent = PatientConsent(**payload.model_dump())
    db.add(consent)
    await db.commit()
    await db.refresh(consent)
    await record_audit_event(
        db,
        event_type="consent.accepted" if consent.accepted else "consent.declined",
        entity_type="patient_consent",
        entity_id=consent.id,
        actor_id=consent.patient_id,
        actor_type="patient",
        payload={"consent_type": consent.consent_type, "version": consent.consent_version},
    )
    return consent


async def list_consents(db: AsyncSession, patient_id: str) -> list[PatientConsent]:
    result = await db.execute(
        select(PatientConsent)
        .where(PatientConsent.patient_id == patient_id)
        .order_by(PatientConsent.created_at.desc())
    )
    return list(result.scalars().all())


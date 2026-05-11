from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.visit import Appointment, Visit
from app.schemas.appointments import AppointmentCreate, VisitSummaryCreate


async def create_appointment(db: AsyncSession, payload: AppointmentCreate) -> Appointment:
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def create_visit_summary(db: AsyncSession, payload: VisitSummaryCreate) -> Visit:
    summary = "Visit summary prepared from intake and transcript for doctor review."
    visit = Visit(
        appointment_id=payload.appointment_id,
        intake_session_id=payload.intake_session_id,
        transcript=payload.transcript,
        ai_summary=summary,
        disposition="doctor_review",
    )
    db.add(visit)
    await db.commit()
    await db.refresh(visit)
    return visit


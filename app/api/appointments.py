from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.appointments import AppointmentCreate, AppointmentRead, VisitSummaryCreate
from app.services.appointment_service import create_appointment, create_visit_summary

router = APIRouter(tags=["appointments", "visits"])


@router.post("/appointments", response_model=AppointmentRead)
async def create_appointment_endpoint(
    payload: AppointmentCreate,
    db: AsyncSession = Depends(get_db_session),
):
    return await create_appointment(db, payload)


@router.post("/visits/summary")
async def create_visit_summary_endpoint(
    payload: VisitSummaryCreate,
    db: AsyncSession = Depends(get_db_session),
):
    return await create_visit_summary(db, payload)


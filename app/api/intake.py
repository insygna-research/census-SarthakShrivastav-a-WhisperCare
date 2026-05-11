from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.intake import IntakeResponse, IntakeSessionCreate, IntakeSessionRead, IntakeUpdate
from app.services.intake_service import create_intake_session, get_intake_session, update_intake_session

router = APIRouter(prefix="/intake/sessions", tags=["intake"])


@router.post("", response_model=IntakeResponse)
async def create_intake_endpoint(
    payload: IntakeSessionCreate,
    db: AsyncSession = Depends(get_db_session),
):
    return await create_intake_session(db, payload)


@router.put("/{session_id}", response_model=IntakeResponse)
async def update_intake_endpoint(
    session_id: str,
    payload: IntakeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    session = await get_intake_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Intake session not found")
    return await update_intake_session(db, session, payload)


@router.get("/{session_id}", response_model=IntakeSessionRead)
async def get_intake_endpoint(session_id: str, db: AsyncSession = Depends(get_db_session)):
    session = await get_intake_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Intake session not found")
    return session


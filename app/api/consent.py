from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.consent import ConsentCreate, ConsentRead
from app.services.consent_service import create_consent, list_consents

router = APIRouter(prefix="/consents", tags=["consents"])


@router.post("", response_model=ConsentRead)
async def create_consent_endpoint(
    payload: ConsentCreate,
    db: AsyncSession = Depends(get_db_session),
):
    return await create_consent(db, payload)


@router.get("/{patient_id}", response_model=list[ConsentRead])
async def list_consents_endpoint(patient_id: str, db: AsyncSession = Depends(get_db_session)):
    return await list_consents(db, patient_id)


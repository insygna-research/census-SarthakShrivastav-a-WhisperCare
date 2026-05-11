from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.schemas.voice import VoiceConnectRequest, VoiceConnectResponse, VoiceDisconnectRequest
from app.services.voice_service import create_voice_session

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/connect", response_model=VoiceConnectResponse)
async def connect_voice_endpoint(
    payload: VoiceConnectRequest,
    db: AsyncSession = Depends(get_db_session),
):
    return await create_voice_session(db, payload)


@router.post("/disconnect")
async def disconnect_voice_endpoint(payload: VoiceDisconnectRequest):
    return {"status": "ok", "voice_session_id": payload.voice_session_id}


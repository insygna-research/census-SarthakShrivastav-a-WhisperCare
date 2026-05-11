from __future__ import annotations

import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.voice import VoiceSession
from app.schemas.voice import VoiceConnectRequest, VoiceConnectResponse


async def create_voice_session(db: AsyncSession, payload: VoiceConnectRequest) -> VoiceConnectResponse:
    settings = get_settings()
    room_name = f"{settings.livekit.room_prefix}-{uuid.uuid4().hex[:12]}"
    voice_session = VoiceSession(
        intake_session_id=payload.intake_session_id,
        patient_id=payload.patient_id,
        room_name=room_name,
    )
    db.add(voice_session)
    await db.commit()
    await db.refresh(voice_session)
    token = _build_livekit_token(room_name, voice_session.id, payload)
    return VoiceConnectResponse(
        token=token,
        livekit_url=settings.livekit.url,
        room_name=room_name,
        voice_session_id=voice_session.id,
        intake_session_id=payload.intake_session_id,
    )


def _build_livekit_token(room_name: str, voice_session_id: str, payload: VoiceConnectRequest) -> str:
    settings = get_settings()
    if not settings.livekit.api_key or not settings.livekit.api_secret:
        return "local-dev-token"
    from livekit.api import AccessToken, VideoGrants

    metadata = {
        "voice_session_id": voice_session_id,
        "intake_session_id": payload.intake_session_id,
        "patient_id": payload.patient_id,
        "language": payload.language or settings.languages.default,
    }
    return (
        AccessToken(settings.livekit.api_key, settings.livekit.api_secret)
        .with_identity(f"patient-{payload.patient_id or voice_session_id}")
        .with_metadata(json.dumps(metadata))
        .with_grants(VideoGrants(room_join=True, room=room_name, can_publish=True, can_subscribe=True))
        .to_jwt()
    )


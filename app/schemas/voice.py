from pydantic import BaseModel


class VoiceConnectRequest(BaseModel):
    patient_id: str | None = None
    intake_session_id: str | None = None
    language: str | None = None


class VoiceConnectResponse(BaseModel):
    token: str
    livekit_url: str
    room_name: str
    voice_session_id: str
    intake_session_id: str | None


class VoiceDisconnectRequest(BaseModel):
    voice_session_id: str
    room_name: str | None = None


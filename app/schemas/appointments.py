from pydantic import BaseModel, Field


class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str | None = None
    mode: str = "teleconsult"
    scheduled_for: str | None = None


class AppointmentRead(BaseModel):
    id: str
    patient_id: str
    doctor_id: str | None
    status: str
    mode: str
    scheduled_for: str | None

    model_config = {"from_attributes": True}


class VisitSummaryCreate(BaseModel):
    appointment_id: str
    intake_session_id: str | None = None
    transcript: list[dict] = Field(default_factory=list)


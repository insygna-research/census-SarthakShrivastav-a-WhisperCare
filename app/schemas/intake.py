from pydantic import BaseModel, Field


class IntakeSessionCreate(BaseModel):
    patient_id: str | None = None
    intake_type: str = "combined"


class IntakeUpdate(BaseModel):
    input_text: str
    source: str = "ui"


class IntakeResponse(BaseModel):
    session_id: str
    assistant_text: str
    current_screen: str
    progress: dict = Field(default_factory=dict)
    risk_level: str
    need_human: bool
    completed: bool
    scores: dict = Field(default_factory=dict)
    summary: str | None = None


class IntakeSessionRead(BaseModel):
    id: str
    patient_id: str | None
    intake_type: str
    status: str
    current_screen: str
    risk_level: str
    need_human: bool
    raw_answers: dict
    scores: dict
    summary: str | None

    model_config = {"from_attributes": True}


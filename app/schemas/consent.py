from pydantic import BaseModel, Field


class ConsentCreate(BaseModel):
    patient_id: str
    consent_type: str
    consent_version: str
    accepted: bool = True
    metadata_json: dict = Field(default_factory=dict)


class ConsentRead(BaseModel):
    id: str
    patient_id: str
    consent_type: str
    consent_version: str
    accepted: bool
    metadata_json: dict

    model_config = {"from_attributes": True}


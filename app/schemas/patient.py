from __future__ import annotations

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    phone: str
    full_name: str
    age: int | None = None
    gender: str | None = None
    state: str | None = None
    preferred_language: str | None = None
    emergency_contact: dict = Field(default_factory=dict)


class PatientUpdate(BaseModel):
    full_name: str | None = None
    age: int | None = None
    gender: str | None = None
    state: str | None = None
    preferred_language: str | None = None
    emergency_contact: dict | None = None
    abha_address: str | None = None
    abha_number: str | None = None


class PatientRead(BaseModel):
    id: str
    phone: str
    full_name: str
    age: int | None
    gender: str | None
    state: str | None
    preferred_language: str
    emergency_contact: dict
    abha_address: str | None
    abha_number: str | None

    model_config = {"from_attributes": True}


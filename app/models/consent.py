from __future__ import annotations

from typing import Any
import uuid

from sqlalchemy import JSON, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class PatientConsent(TimestampMixin, Base):
    __tablename__ = "patient_consents"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    consent_type: Mapped[str] = mapped_column(String, nullable=False)
    consent_version: Mapped[str] = mapped_column(String, nullable=False)
    accepted: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


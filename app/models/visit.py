from __future__ import annotations

from typing import Any
import uuid

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class Doctor(TimestampMixin, Base):
    __tablename__ = "doctors"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    registration_number: Mapped[str] = mapped_column(String, nullable=False)
    specialty: Mapped[str] = mapped_column(String, nullable=False)
    languages: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)


class Appointment(TimestampMixin, Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    doctor_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    status: Mapped[str] = mapped_column(String, default="requested", nullable=False)
    mode: Mapped[str] = mapped_column(String, default="teleconsult", nullable=False)
    scheduled_for: Mapped[str | None] = mapped_column(String, nullable=True)


class Visit(TimestampMixin, Base):
    __tablename__ = "visits"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    appointment_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    intake_session_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    transcript: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    ai_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    doctor_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    disposition: Mapped[str | None] = mapped_column(String, nullable=True)


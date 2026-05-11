from __future__ import annotations

import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class VoiceSession(TimestampMixin, Base):
    __tablename__ = "voice_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    intake_session_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    patient_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    room_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String, default="created", nullable=False)


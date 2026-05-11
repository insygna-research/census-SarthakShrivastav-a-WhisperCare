from __future__ import annotations

from typing import Any
import uuid

from sqlalchemy import JSON, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class IntakeSession(TimestampMixin, Base):
    __tablename__ = "intake_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    intake_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active", nullable=False)
    current_screen: Mapped[str] = mapped_column(String, default="start", nullable=False)
    risk_level: Mapped[str] = mapped_column(String, default="low", nullable=False)
    need_human: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    raw_answers: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    scores: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)


class IntakeTurn(TimestampMixin, Base):
    __tablename__ = "intake_turns"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String, default="ui", nullable=False)
    graph_node: Mapped[str | None] = mapped_column(String, nullable=True)
    risk_signal: Mapped[str | None] = mapped_column(String, nullable=True)


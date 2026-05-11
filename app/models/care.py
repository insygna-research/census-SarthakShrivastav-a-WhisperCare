from __future__ import annotations

from typing import Any
import uuid

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin


class CarePlan(TimestampMixin, Base):
    __tablename__ = "care_plans"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    visit_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    goals: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    tasks: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    follow_up_schedule: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active", nullable=False)


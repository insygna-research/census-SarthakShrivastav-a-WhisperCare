from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditEvent


async def record_audit_event(
    db: AsyncSession,
    *,
    event_type: str,
    entity_type: str,
    entity_id: str | None = None,
    actor_id: str | None = None,
    actor_type: str = "system",
    payload: dict[str, Any] | None = None,
) -> AuditEvent:
    event = AuditEvent(
        actor_id=actor_id,
        actor_type=actor_type,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        payload=payload or {},
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


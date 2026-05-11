from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.graphs.intake.graph import intake_graph
from app.models.intake import IntakeSession, IntakeTurn
from app.schemas.intake import IntakeResponse, IntakeSessionCreate, IntakeUpdate
from app.services.audit_service import record_audit_event


async def create_intake_session(db: AsyncSession, payload: IntakeSessionCreate) -> IntakeResponse:
    session = IntakeSession(patient_id=payload.patient_id, intake_type=payload.intake_type)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    state = await intake_graph.ainvoke(
        {
            "session_id": session.id,
            "patient_id": session.patient_id,
            "intake_type": session.intake_type,
            "input_text": "",
            "current_screen": "start",
            "answers": {},
            "scores": {},
            "risk_level": "low",
            "need_human": False,
        }
    )
    session.current_screen = state["current_screen"]
    await db.commit()
    return _to_response(session, state)


async def update_intake_session(
    db: AsyncSession,
    session: IntakeSession,
    payload: IntakeUpdate,
) -> IntakeResponse:
    db.add(IntakeTurn(session_id=session.id, role="user", content=payload.input_text, source=payload.source))
    state = await intake_graph.ainvoke(
        {
            "session_id": session.id,
            "patient_id": session.patient_id,
            "intake_type": session.intake_type,
            "input_text": payload.input_text,
            "source": payload.source,
            "current_screen": session.current_screen,
            "answers": session.raw_answers,
            "scores": session.scores,
            "risk_level": session.risk_level,
            "need_human": session.need_human,
        }
    )
    session.current_screen = state.get("current_screen", session.current_screen)
    session.raw_answers = state.get("answers", {})
    session.scores = state.get("scores", {})
    session.risk_level = state.get("risk_level", "low")
    session.need_human = state.get("need_human", False)
    session.summary = state.get("summary")
    if state.get("completed"):
        session.status = "completed"
    assistant_text = state.get("assistant_text", "")
    if assistant_text:
        db.add(IntakeTurn(session_id=session.id, role="assistant", content=assistant_text, source="system"))
    await db.commit()
    await db.refresh(session)
    if session.need_human:
        await record_audit_event(
            db,
            event_type="intake.escalated",
            entity_type="intake_session",
            entity_id=session.id,
            actor_id=session.patient_id,
            actor_type="patient",
            payload={"risk_level": session.risk_level},
        )
    return _to_response(session, state)


async def get_intake_session(db: AsyncSession, session_id: str) -> IntakeSession | None:
    result = await db.execute(select(IntakeSession).where(IntakeSession.id == session_id))
    return result.scalar_one_or_none()


def _to_response(session: IntakeSession, state: dict) -> IntakeResponse:
    return IntakeResponse(
        session_id=session.id,
        assistant_text=state.get("assistant_text", ""),
        current_screen=state.get("current_screen", session.current_screen),
        progress=state.get("progress", {}),
        risk_level=state.get("risk_level", session.risk_level),
        need_human=state.get("need_human", session.need_human),
        completed=state.get("completed", session.status == "completed"),
        scores=state.get("scores", session.scores),
        summary=state.get("summary", session.summary),
    )


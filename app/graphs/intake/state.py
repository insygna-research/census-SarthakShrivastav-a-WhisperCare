from typing_extensions import TypedDict


class IntakeGraphState(TypedDict, total=False):
    session_id: str
    patient_id: str | None
    intake_type: str
    input_text: str
    source: str
    current_screen: str
    answers: dict
    scores: dict
    risk_level: str
    need_human: bool
    assistant_text: str
    completed: bool
    summary: str | None
    progress: dict


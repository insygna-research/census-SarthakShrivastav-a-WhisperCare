from __future__ import annotations

from app.core.config import get_settings
from app.graphs.intake.state import IntakeGraphState
from app.services.safety_service import detect_risk
from app.services.screening_service import normalize_answer, score_tool


def check_risk_node(state: IntakeGraphState) -> dict:
    risk = detect_risk(state.get("input_text", ""), state.get("scores", {}))
    if risk["need_human"]:
        return {
            "risk_level": risk["risk_level"],
            "need_human": True,
            "assistant_text": risk["response"],
            "completed": True,
            "summary": "Urgent human review required due to safety signal.",
        }
    return {"risk_level": "low", "need_human": False}


def route_intake_node(state: IntakeGraphState) -> dict:
    settings = get_settings()
    answers = dict(state.get("answers", {}))
    current_screen = state.get("current_screen", "phq9_0")
    tool_name = "gad7" if current_screen.startswith("gad7") else "phq9"
    index = int(current_screen.split("_")[-1]) if "_" in current_screen else 0
    normalized = normalize_answer(state.get("input_text", ""))

    if normalized and current_screen != "start":
        answers[current_screen] = normalized

    phq9_count = len(settings.screening.phq9.questions)
    gad7_count = len(settings.screening.gad7.questions)

    if tool_name == "phq9" and normalized and index + 1 >= phq9_count:
        next_screen = "gad7_0" if state.get("intake_type") in {"combined", "gad7"} else "summary"
    elif tool_name == "gad7" and normalized and index + 1 >= gad7_count:
        next_screen = "summary"
    elif normalized:
        next_screen = f"{tool_name}_{index + 1}"
    else:
        next_screen = "phq9_0" if current_screen == "start" else current_screen

    return {"answers": answers, "current_screen": next_screen}


def score_response_node(state: IntakeGraphState) -> dict:
    answers = state.get("answers", {})
    phq9_answers = {k: v for k, v in answers.items() if k.startswith("phq9")}
    gad7_answers = {k: v for k, v in answers.items() if k.startswith("gad7")}
    scores = {}
    if phq9_answers:
        scores["phq9"] = score_tool("phq9", phq9_answers)
    if gad7_answers:
        scores["gad7"] = score_tool("gad7", gad7_answers)
    item9 = phq9_answers.get("phq9_8")
    if item9:
        scores["phq9_item9"] = get_settings().screening.phq9.answer_scores.get(item9, 0)
    return {"scores": scores}


def build_reply_node(state: IntakeGraphState) -> dict:
    settings = get_settings()
    screen = state.get("current_screen", "phq9_0")
    if state.get("need_human"):
        return {}
    if screen == "summary":
        return {"assistant_text": "Thank you. I have completed the intake and prepared a summary.", "completed": True}
    tool_name = "gad7" if screen.startswith("gad7") else "phq9"
    index = int(screen.split("_")[-1])
    question = getattr(settings.screening, tool_name).questions[index]
    return {
        "assistant_text": (
            f"{question}. Please answer: not at all, several days, "
            "more than half the days, or nearly every day."
        ),
        "completed": False,
        "progress": {"tool": tool_name, "index": index},
    }


def write_summary_node(state: IntakeGraphState) -> dict:
    if not state.get("completed"):
        return {}
    scores = state.get("scores", {})
    summary = (
        f"Intake completed. PHQ-9: {scores.get('phq9', {}).get('total', 'n/a')} "
        f"({scores.get('phq9', {}).get('severity', 'n/a')}), "
        f"GAD-7: {scores.get('gad7', {}).get('total', 'n/a')} "
        f"({scores.get('gad7', {}).get('severity', 'n/a')}). "
        f"Risk level: {state.get('risk_level', 'low')}."
    )
    return {"summary": summary}


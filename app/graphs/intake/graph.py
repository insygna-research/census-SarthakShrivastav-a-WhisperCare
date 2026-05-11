from langgraph.graph import END, START, StateGraph

from app.graphs.intake.nodes import (
    build_reply_node,
    check_risk_node,
    route_intake_node,
    score_response_node,
    write_summary_node,
)
from app.graphs.intake.state import IntakeGraphState


def _after_risk(state: IntakeGraphState) -> str:
    return "write_summary" if state.get("need_human") else "route_intake"


def _after_reply(state: IntakeGraphState) -> str:
    return "write_summary" if state.get("completed") else END


def build_intake_graph():
    builder = StateGraph(IntakeGraphState)
    builder.add_node("check_risk", check_risk_node)
    builder.add_node("route_intake", route_intake_node)
    builder.add_node("score_response", score_response_node)
    builder.add_node("build_reply", build_reply_node)
    builder.add_node("write_summary", write_summary_node)

    builder.add_edge(START, "check_risk")
    builder.add_conditional_edges("check_risk", _after_risk)
    builder.add_edge("route_intake", "score_response")
    builder.add_edge("score_response", "build_reply")
    builder.add_conditional_edges("build_reply", _after_reply)
    builder.add_edge("write_summary", END)
    return builder.compile()


intake_graph = build_intake_graph()


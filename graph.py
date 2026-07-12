"""
Builds the LangGraph StateGraph:

    START -> Intent Classifier -> (admission | exam | fees | scholarship | general) -> Response Agent -> END

The "general" branch is a safety net: when the classifier (online or
offline) can't confidently match a real department, this branch gives
an honest "I'm not sure, here's what I can help with" reply instead of
guessing wrong department info.
"""

from langgraph.graph import StateGraph, START, END

from state import CollegeState
from classifier import classify_intent
from agents import admission_agent, exam_agent, fees_agent, scholarship_agent, general_agent
from response_agent import generate_response


def route_by_intent(state: CollegeState) -> str:
    return state["intent"]


def build_graph():
    graph = StateGraph(CollegeState)

    # --- Register nodes ---
    graph.add_node("intent_classifier", classify_intent)
    graph.add_node("admission_agent", admission_agent)
    graph.add_node("exam_agent", exam_agent)
    graph.add_node("fees_agent", fees_agent)
    graph.add_node("scholarship_agent", scholarship_agent)
    graph.add_node("general_agent", general_agent)
    graph.add_node("response_agent", generate_response)

    # --- START -> Intent Classifier ---
    graph.add_edge(START, "intent_classifier")

    # --- Intent Classifier -> one of 5 agents (conditional) ---
    graph.add_conditional_edges(
        "intent_classifier",
        route_by_intent,
        {
            "admission": "admission_agent",
            "exam": "exam_agent",
            "fees": "fees_agent",
            "scholarship": "scholarship_agent",
            "general": "general_agent",
        },
    )

    # --- All agents -> Response Agent ---
    graph.add_edge("admission_agent", "response_agent")
    graph.add_edge("exam_agent", "response_agent")
    graph.add_edge("fees_agent", "response_agent")
    graph.add_edge("scholarship_agent", "response_agent")
    graph.add_edge("general_agent", "response_agent")

    # --- Response Agent -> END ---
    graph.add_edge("response_agent", END)

    return graph.compile()
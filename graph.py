"""
Builds the LangGraph StateGraph.

Flow:

START
  ↓
Intent Classifier
  ↓
Department Agent
  ↓
Ticket Decision
  ↓
Ticket Required?
 ↙              ↘
YES              NO
 ↓                ↓
Ticket Agent    Response Agent
 ↓                ↓
END              END
"""

from langgraph.graph import StateGraph, START, END

from state import CollegeState
from classifier import classify_intent
from agents import (
    admission_agent,
    exam_agent,
    fees_agent,
    scholarship_agent,
    general_agent,
)
from response_agent import generate_response
from ticket_decision import decide_ticket_required
from ticket_agent import create_ticket


def route_by_intent(state: CollegeState) -> str:
    return state["intent"]


def route_ticket(state: CollegeState) -> str:
    if state["ticket_required"]:
        return "ticket"

    return "response"


def build_graph():
    graph = StateGraph(CollegeState)

    # --- Register nodes ---
    graph.add_node("intent_classifier", classify_intent)
    graph.add_node("admission_agent", admission_agent)
    graph.add_node("exam_agent", exam_agent)
    graph.add_node("fees_agent", fees_agent)
    graph.add_node("scholarship_agent", scholarship_agent)
    graph.add_node("general_agent", general_agent)

    graph.add_node("ticket_decision", decide_ticket_required)
    graph.add_node("ticket_agent", create_ticket)
    graph.add_node("response_agent", generate_response)

    # --- START -> Intent Classifier ---
    graph.add_edge(START, "intent_classifier")

    # --- Intent routing ---
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

    # --- Department Agents -> Ticket Decision ---
    graph.add_edge("admission_agent", "ticket_decision")
    graph.add_edge("exam_agent", "ticket_decision")
    graph.add_edge("fees_agent", "ticket_decision")
    graph.add_edge("scholarship_agent", "ticket_decision")
    graph.add_edge("general_agent", "ticket_decision")

    # --- Ticket Decision Routing ---
    graph.add_conditional_edges(
        "ticket_decision",
        route_ticket,
        {
            "ticket": "ticket_agent",
            "response": "response_agent",
        },
    )

    # --- Final edges ---
    graph.add_edge("ticket_agent", END)
    graph.add_edge("response_agent", END)

    return graph.compile()
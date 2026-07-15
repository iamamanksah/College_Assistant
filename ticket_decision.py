"""
Decides whether a student issue requires human helpdesk support.
"""

from state import CollegeState


ESCALATION_KEYWORDS = {
    "deducted",
    "not received",
    "not showing",
    "failed",
    "blocked",
    "locked",
    "incorrect",
    "wrong",
    "complaint",
    "urgent",
    "not updated",
    "issue",
    "problem",
}


def decide_ticket_required(state: CollegeState) -> dict:
    """Check whether the query should be escalated to a support ticket."""

    query = state["query"].lower()

    ticket_required = any(
        keyword in query
        for keyword in ESCALATION_KEYWORDS
    )

    if ticket_required:
        print("⚠️ Issue requires human helpdesk support")

    return {
        "ticket_required": ticket_required,
    }
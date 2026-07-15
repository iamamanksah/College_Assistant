"""
Shared state that flows through every node in the graph.

This is a "shared memory" object (as taught in class): every node
reads it before it runs, and updates it before it hands off to the
next node. This removes the need for manual data passing between
nodes/agents.

Field names match the class activity: query, intent, department
(the data the specialist agent found), and response (the final
answer). chat_history is added so the assistant can answer
follow-up questions using past turns.

Ticket fields are added to support helpdesk ticket creation for
issues that require human assistance.
"""

from typing import TypedDict, Optional, List


class CollegeState(TypedDict):
    # The raw question typed by the user
    query: str

    # Filled in by the Intent Classifier node.
    # One of: "admission", "exam", "fees", "scholarship", "general"
    intent: Optional[str]

    # Filled in by whichever specialist agent handles the query —
    # the raw data/fact it found by searching its own document/database
    department: Optional[str]

    # Filled in by the Response Agent — the final, user-facing answer
    response: Optional[str]

    # Running conversation history, so follow-up questions can be
    # answered using context from earlier turns
    chat_history: List[str]

    # Whether the issue needs human helpdesk support
    ticket_required: bool

    # Unique ID of the generated support ticket
    ticket_id: Optional[str]

    # Current status of the support ticket
    ticket_status: Optional[str]
"""
Ticket Agent for the College Helpdesk.

Creates support tickets for student issues that require
human helpdesk assistance.
"""

import json
import os
from datetime import datetime

from state import CollegeState


TICKET_FILE = "data/tickets.json"


def _load_tickets() -> list:
    if not os.path.exists(TICKET_FILE):
        return []

    with open(TICKET_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def _save_tickets(tickets: list) -> None:
    os.makedirs("data", exist_ok=True)

    with open(TICKET_FILE, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def create_ticket(state: CollegeState) -> dict:
    """Create and store a new helpdesk ticket."""

    tickets = _load_tickets()

    ticket_number = len(tickets) + 1

    ticket_id = (
        f"TKT-{datetime.now().strftime('%Y%m%d')}-"
        f"{ticket_number:03d}"
    )

    ticket = {
        "ticket_id": ticket_id,
        "query": state["query"],
        "department": state["intent"],
        "status": "open",
        "created_at": datetime.now().isoformat(),
    }

    tickets.append(ticket)
    _save_tickets(tickets)

    print(f"🎫 Support Ticket Created: {ticket_id}")

    return {
        "ticket_id": ticket_id,
        "ticket_status": "open",
    }
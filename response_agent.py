"""
Hybrid Response Agent.

Uses Groq first.
Falls back to Python formatting if Groq fails.
"""

from state import CollegeState
from llm import call_llm


SYSTEM_PROMPT = """
You are the final Response Agent for a college helpdesk chatbot.

Rewrite the provided college information as a warm,
clear and well-formatted response.

Do not invent new facts.
"""


def generate_response(state: CollegeState) -> dict:

    raw_fact = state["department"]

    try:

        final = call_llm(
            SYSTEM_PROMPT,
            raw_fact
        )

        print("🌐 Groq Response Agent Used")

        return {
            "response": final
        }

    except Exception:

        print("💻 Offline Response Agent Used")

        final = (
            "Hello!\n\n"
            f"{raw_fact}\n\n"
            "If you have another question, feel free to ask."
        )

        return {
            "response": final
        }
"""
Hybrid Intent Classifier.

Uses Groq first.
If Groq fails, uses offline Python keyword classification.
"""

from state import CollegeState
from llm import call_llm


VALID_INTENTS = [
    "admission",
    "exam",
    "fees",
    "scholarship"
]


SYSTEM_PROMPT = """
You are an intent classifier for a college helpdesk chatbot.

Classify the user query into EXACTLY ONE category:

admission
exam
fees
scholarship

Reply with ONLY the category word, nothing else — no punctuation,
no extra sentence, no explanation.
"""


KEYWORD_MAP = {
    "admission": [
        "admission", "admit", "eligibility", "eligible", "apply",
        "application", "document", "percentage", "course", "seat",
        "enroll", "enrollment", "branch", "cutoff",
    ],
    "exam": [
        "exam", "result", "hall ticket", "semester", "syllabus",
        "attendance", "marks", "grade", "test", "revaluation",
        "timetable", "schedule",
    ],
    "fees": [
        "fee", "fees", "payment", "refund", "amount", "due",
        "installment", "bank", "challan",
    ],
    "scholarship": [
        "scholarship", "financial aid", "merit", "stipend",
        "grant", "waiver", "reservation",
    ],
}


def offline_classifier(query: str) -> str | None:
    """Simple keyword matcher used only when Groq is unreachable."""
    query = query.lower()
    for intent, keywords in KEYWORD_MAP.items():
        if any(word in query for word in keywords):
            return intent
    return None


def classify_intent(state: CollegeState) -> dict:
    query = state["query"]

    try:
        raw = call_llm(SYSTEM_PROMPT, query).strip().lower()

        # LENIENT match: Groq sometimes replies with extra
        # punctuation or a short sentence (e.g. "Admission." or
        # "The category is fees") instead of the bare word. Instead
        # of requiring an exact match, check whether a valid intent
        # word APPEARS in the reply.
        matched = next((v for v in VALID_INTENTS if v in raw), None)

        if matched:
            print("🌐 Groq Intent Classifier Used")
            return {"intent": matched}

        print(f"⚠️  Groq replied but didn't match a category (got: {raw!r}) — falling back offline.")

    except Exception as e:
        print(f"⚠️  Groq call failed ({type(e).__name__}) — falling back offline.")

    print("💻 Offline Intent Classifier Used")

    intent = offline_classifier(query)

    if intent is None:
        # Nothing matched — be honest instead of guessing "admission".
        print("❓ Offline classifier couldn't confidently match a category — using 'general'.")
        intent = "general"

    return {"intent": intent}
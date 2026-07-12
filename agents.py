"""
The five specialist agent nodes: Admission, Exam, Fees, Scholarship,
and General (fallback when the classifier can't confidently match a
real department).

Each department agent:
  1) reads the query from state,
  2) runs a SEARCH over its own department's documents only,
  3) writes the raw finding into state["department"] for the
     Response Agent to turn into a friendly reply.
"""

from state import CollegeState
from database import (
    ADMISSION_DOCS,
    EXAM_DOCS,
    FEES_DOCS,
    SCHOLARSHIP_DOCS,
    search_department_docs,
)


def admission_agent(state: CollegeState) -> dict:
    result = search_department_docs(ADMISSION_DOCS, state["query"])
    return {"department": result}


def exam_agent(state: CollegeState) -> dict:
    result = search_department_docs(EXAM_DOCS, state["query"])
    return {"department": result}


def fees_agent(state: CollegeState) -> dict:
    result = search_department_docs(FEES_DOCS, state["query"])
    return {"department": result}


def scholarship_agent(state: CollegeState) -> dict:
    result = search_department_docs(SCHOLARSHIP_DOCS, state["query"])
    return {"department": result}


def general_agent(state: CollegeState) -> dict:
    """
    Handles queries the classifier couldn't confidently match to a
    real department — instead of guessing "admission" and showing
    wrong info, it tells the user honestly what the bot can help with.
    """
    message = (
        "I couldn't quite tell which department your question falls "
        "under. I can help with: Admission, Exam, Fees, or Scholarship. "
        "Could you rephrase your question mentioning one of these?"
    )
    return {"department": message}
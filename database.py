"""
Simulated document store — one "database" per department.

Each department agent can ONLY search its own dict, never another
department's data.
"""

ADMISSION_DOCS = {
    "b.tech": "Admission starts in July. Eligibility: 60% in Class 12 (PCM). "
              "Process: apply online, pay fee, document verification, "
              "then seat allotment.",
    "default": "Admissions generally open in July. Check the specific "
               "course page for eligibility and required documents.",
}

EXAM_DOCS = {
    "semester": "Semester exams are held in the last week of December "
                "and May. Hall tickets are released 10 days before exams.",
    "default": "Exam schedules are published on the college notice board "
               "and student portal at least 3 weeks in advance.",
}
FEES_DOCS = {
    "b.tech": "B.Tech annual fee: as per the latest fee structure on the "
              "college website. Last date for payment: 15th of every "
              "semester start month. Late fee applies after that.",
    "default": "Fee payment is done online via the student portal. "
               "Check the fee structure page for course-wise amounts.",
}
SCHOLARSHIP_DOCS = {
    "second year": "Merit scholarship applications for 2nd year students "
                   "open on 21st December. Minimum 75% required in "
                   "previous year to be eligible.",
    "default": "Scholarship details vary by category (merit, need-based, "
               "government). Applications typically open in December.",
}
def search_department_docs(docs: dict, query: str) -> str:
    """Simple keyword search over a department's documents."""
    query_lower = query.lower()
    for key, content in docs.items():
        if key != "default" and key in query_lower:
            return content
    return docs["default"]
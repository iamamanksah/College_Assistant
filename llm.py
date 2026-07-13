"""
LLM provider for the College Helpdesk LangGraph project.
Uses Groq's free API (fast, generous free tier, no credit card needed).
"""

import os
import time

from dotenv import load_dotenv
load_dotenv()

from groq import Groq


class QuotaExhaustedError(RuntimeError):
    """Raised when the rate/daily limit is used up — retrying won't help."""
    pass


_quota_known_exhausted = False

# Running totals for this process/session
_session_token_usage = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "calls": 0,
}


def _is_quota_error(exc: Exception) -> bool:
    msg = str(exc)
    return "429" in msg or "rate_limit" in msg.lower() or "RESOURCE_EXHAUSTED" in msg


def _record_usage(usage) -> None:
    """Update session totals and print a per-call token usage line."""
    if usage is None:
        return

    prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
    completion_tokens = getattr(usage, "completion_tokens", 0) or 0
    total_tokens = getattr(usage, "total_tokens", prompt_tokens + completion_tokens)

    _session_token_usage["prompt_tokens"] += prompt_tokens
    _session_token_usage["completion_tokens"] += completion_tokens
    _session_token_usage["total_tokens"] += total_tokens
    _session_token_usage["calls"] += 1

    print(
        f"🔢 Tokens — this call: {total_tokens} "
        f"(prompt: {prompt_tokens}, completion: {completion_tokens}) | "
        f"session total: {_session_token_usage['total_tokens']} "
        f"over {_session_token_usage['calls']} call(s)"
    )


def get_session_token_usage() -> dict:
    """Return a copy of the accumulated token usage stats for this session."""
    return dict(_session_token_usage)


def reset_session_token_usage() -> None:
    """Reset the accumulated token usage stats (e.g. between test runs)."""
    _session_token_usage.update(
        {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "calls": 0}
    )


def call_llm(system_prompt: str, user_prompt: str) -> str:
    global _quota_known_exhausted

    if _quota_known_exhausted:
        raise QuotaExhaustedError("Quota already known to be exhausted this session.")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Create a .env file in this folder "
            "with the line: GROQ_API_KEY=your_key_here "
            "(get a free key at https://console.groq.com)"
        )

    client = Groq(api_key=api_key)

    model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    max_retries = 2
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
            )

            _record_usage(getattr(response, "usage", None))

            return response.choices[0].message.content.strip()

        except Exception as e:
            last_error = e

            if _is_quota_error(e):
                _quota_known_exhausted = True
                print("⚠️  Groq quota/rate-limit hit — switching to offline mode for this session.")
                raise QuotaExhaustedError(str(e)) from e

            if attempt < max_retries - 1:
                print(f"⚠️  Groq API error, retrying ({attempt + 1}/{max_retries})...")
                time.sleep(2)

    raise RuntimeError(f"Groq API unavailable after retries: {last_error}")
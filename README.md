# College Helpdesk Chatbot — LangGraph Multi-Agent Project

An interactive chatbot that classifies a student's query and routes it
to the right department agent (Admission, Exam, Fees, or Scholarship),
which fetches the relevant info and hands it to a Response Agent that
formats a friendly final reply.

```
START -> Intent Classifier -> [Admission | Exam | Fees | Scholarship | General] Agent -> Response Agent -> END
```

## Project structure

```
files/
├── state.py            # Shared state: query, intent, department, response
├── database.py          # Per-department "documents" + keyword search
├── llm.py               # LLM wrapper — Groq API with offline fallback
├── classifier.py         # Intent Classifier node
├── agents.py             # Admission / Exam / Fees / Scholarship / General agents
├── response_agent.py      # Formats the final reply (Groq, with offline fallback)
├── graph.py              # Builds & compiles the LangGraph StateGraph
├── main.py               # Interactive CLI chatbot — run this
├── .env                  # API key (not committed — see setup below)
└── requirements.txt
```

## How it works

1. **Intent Classifier** reads the user's query and classifies it into
   `admission`, `exam`, `fees`, or `scholarship` using Groq's LLM. If
   Groq is unreachable (rate limit, no internet, etc.) it falls back
   to a local keyword matcher — the bot never crashes, it just
   degrades gracefully. If nothing matches confidently, it routes to
   a `general` agent that asks the user to clarify instead of
   guessing wrong.
2. **Graph routing** (`graph.py`) uses `add_conditional_edges()` to
   send the query to the matching specialist agent node.
3. Each specialist agent (`agents.py`) looks up its own department's
   data in `database.py` — no agent can see another department's
   data (e.g. the Admission agent never touches fee info).
4. **Response Agent** takes that raw fact and rewrites it as a warm,
   well-formatted reply using Groq — again with an offline formatting
   fallback if the API is unavailable.
5. Conversation history is kept in `chat_history` across turns.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a free Groq API key (no credit card needed):
   - Go to https://console.groq.com
   - Sign up (Google/GitHub login)
   - Go to **API Keys** → **Create API Key**
   - Copy the key

3. Create a `.env` file in this folder with:
   ```
   GROQ_API_KEY=your_key_here
   ```

4. Run the chatbot:
   ```bash
   python main.py
   ```

   Type your question (e.g. "how do I apply for admission") and the
   bot will respond. Type `exit` to quit.

## Notes on resilience

This project deliberately handles two real-world failure modes so it
never crashes during a demo:

- **API rate limits / quota exhaustion** — `llm.py` detects this and
  switches to an offline keyword-based classifier + plain-text
  formatter for the rest of the session, instead of retrying
  endlessly or crashing.
- **Ambiguous queries** — if the classifier (online or offline) can't
  confidently match a real department, it routes to a `general` agent
  that gives an honest "I'm not sure, here's what I can help with"
  reply rather than guessing the wrong department.

## Extending this

- Swap the static dicts in `database.py` for a real database or
  document retriever (RAG) — the graph structure doesn't need to change.
- Add more departments by adding a new agent function, a new entry
  in `database.py`, and one more branch in `graph.py`'s conditional
  edges.
- Add a `human-in-the-loop` review step before `response_agent` if needed.
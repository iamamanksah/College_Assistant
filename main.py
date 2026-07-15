"""
Interactive College Helpdesk Chatbot
Run:
    python main.py
"""

from graph import build_graph
from llm import get_session_token_usage


EXIT_WORDS = {"exit", "quit", "q", "bye"}


def print_session_summary():
    usage = get_session_token_usage()

    print("\n" + "=" * 60)
    print("📊 SESSION TOKEN USAGE SUMMARY")
    print("=" * 60)
    print(f"🤖 LLM Calls         : {usage['calls']}")
    print(f"📥 Prompt Tokens     : {usage['prompt_tokens']}")
    print(f"📤 Completion Tokens : {usage['completion_tokens']}")
    print(f"🔢 Total Tokens      : {usage['total_tokens']}")
    print("=" * 60)


def main():
    app = build_graph()

    print("=" * 60)
    print("🎓 College Helpdesk Chatbot")
    print("Type 'exit' to quit.")
    print("=" * 60)

    chat_history = []

    while True:
        try:
            query = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print_session_summary()
            print("\n👋 Thank you for using the College Helpdesk Chatbot!")
            break

        query = query.strip()

        if not query:
            continue

        if query.lower() in EXIT_WORDS:
            print_session_summary()
            print("\n👋 Thank you for using the College Helpdesk Chatbot!")
            break

        try:
            result = app.invoke(
                {
                    "query": query,
                    "chat_history": chat_history,
                }
            )
        except Exception as e:
            print(f"\n⚠️  Something went wrong while processing that: {e}")
            print("Please try again, or type 'exit' to quit.")
            continue

        print("\n" + "=" * 60)
        print("🎯 Intent Detected :", result["intent"])
        print("📂 Department      :", result["department"])

        # Display support ticket or normal chatbot response
        if result.get("ticket_id"):
            print("\n🎫 SUPPORT TICKET CREATED")
            print(f"🆔 Ticket ID   : {result['ticket_id']}")
            print(f"📂 Department  : {result['intent']}")
            print(f"📌 Status      : {result['ticket_status']}")
            print(
                "\nYour issue has been forwarded "
                "to the helpdesk team."
            )
        else:
            print("\n🤖 Bot:")
            print(result["response"])

        print("=" * 60)

        # Store user message in chat history
        chat_history.append(
            {"role": "user", "content": query}
        )

        # Store ticket response or normal AI response
        if result.get("ticket_id"):
            assistant_message = (
                f"Support ticket {result['ticket_id']} created "
                f"for the {result['intent']} department."
            )
        else:
            assistant_message = result["response"]

        chat_history.append(
            {
                "role": "assistant",
                "content": assistant_message,
            }
        )


if __name__ == "__main__":
    main()
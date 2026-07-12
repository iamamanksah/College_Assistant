"""
Interactive College Helpdesk Chatbot
Run:
    python main.py
"""

from graph import build_graph


def main():
    app = build_graph()

    print("=" * 60)
    print("🎓 College Helpdesk Chatbot")
    print("Type 'exit' to quit.")
    print("=" * 60)

    chat_history = []

    while True:
        query = input("\nYou: ")

        if query.lower() in ["exit", "quit"]:
            print("\n👋 Thank you for using the College Helpdesk Chatbot!")
            break

        result = app.invoke(
            {
                "query": query,
                "chat_history": chat_history,
            }
        )

        print("\n" + "=" * 60)
        print("🎯 Intent Detected :", result["intent"])
        print("📂 Department      :", result["department"])
        print("\n🤖 Bot:")
        print(result["response"])
        print("=" * 60)

        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": result["response"]})


if __name__ == "__main__":
    main()
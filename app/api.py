from rich.console import Console

from app.chatbot import Chatbot

console = Console()


def main():
    console.print("[bold green]FP Gemini Edition 1[/bold green]")
    console.print("Type 'exit' to quit. Type 'resume' to continue your last session.\n")

    chatbot = Chatbot()
    session_id = "default"

    while True:
        user_input = console.input("You: ")
        text = user_input.strip()
        if text.lower() in {"exit", "quit", "bye"}:
            console.print("Goodbye!")
            break
        if text.lower() == "resume":
            last_session = chatbot.resume_last_session()
            console.print(f"Resuming session: {last_session.session_id}")
            if last_session.user_message_history:
                console.print("Previous messages:")
                for msg in last_session.user_message_history:
                    console.print(f"  - {msg}")
            continue

        response = chatbot.respond(text, session_id=session_id)
        console.print(f"Assistant: {response}")


if __name__ == "__main__":
    main()

from rich.console import Console

from app.chatbot import Chatbot

console = Console()


def main():
    console.print("[bold green]FP Chatbot Edition 1[/bold green]")
    console.print("Type 'exit' to quit.\n")

    chatbot = Chatbot()
    while True:
        user_input = console.input("You: ")
        if user_input.strip().lower() in {"exit", "quit", "bye"}:
            console.print("Goodbye!")
            break
        response = chatbot.respond(user_input)
        console.print(f"Assistant: {response}")


if __name__ == "__main__":
    main()

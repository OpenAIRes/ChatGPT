import os
import argparse
import logging
import openai
from typing import List, Dict


logger = logging.getLogger(__name__)


def configure_logging(level: str = "INFO") -> None:
    """Configure basic logging for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def ask(
    messages: List[Dict[str, str]],
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
) -> str:
    """Send conversation history to the OpenAI API and return the assistant's response.

    Parameters
    ----------
    messages:
        The chat history to send to the API.
    model:
        Identifier of the model to use.
    temperature:
        Sampling temperature. Higher values yield more random outputs.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
    except Exception as exc:  # noqa: BLE001 - openai may raise various errors
        logger.exception("OpenAI API request failed")
        raise
    return response.choices[0].message["content"]


def main() -> None:
    """Start an interactive chat session with optional history persistence."""

    configure_logging()

    parser = argparse.ArgumentParser(description="Simple ChatGPT command-line interface")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="Model identifier")
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature for response generation",
    )
    parser.add_argument(
        "--history-file",
        help="File path to store the conversation history",
    )
    args = parser.parse_args()

    messages: List[Dict[str, str]] = []

    # Load previous history if the file exists
    if args.history_file and os.path.exists(args.history_file):
        with open(args.history_file, "r", encoding="utf-8") as f:
            for line in f:
                role, content = line.rstrip("\n").split("\t", 1)
                messages.append({"role": role, "content": content})

    while True:
        prompt = input("You: ")
        if not prompt:
            break

        messages.append({"role": "user", "content": prompt})
        answer = ask(messages, model=args.model, temperature=args.temperature)
        messages.append({"role": "assistant", "content": answer})

        if args.history_file:
            with open(args.history_file, "a", encoding="utf-8") as f:
                f.write(f"user\t{prompt}\n")
                f.write(f"assistant\t{answer}\n")

        print("Assistant:", answer)


if __name__ == "__main__":
    main()

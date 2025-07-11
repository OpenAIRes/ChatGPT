import os
import openai
from typing import List, Dict


def ask(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo") -> str:
    """Send conversation history to the OpenAI API and return the assistant's response."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message["content"]


def main() -> None:
    """Start an interactive chat session maintaining conversation history."""
    messages: List[Dict[str, str]] = []
    while True:
        prompt = input("You: ")
        if not prompt:
            break
        messages.append({"role": "user", "content": prompt})
        answer = ask(messages)
        messages.append({"role": "assistant", "content": answer})
        print("Assistant:", answer)


if __name__ == "__main__":
    main()

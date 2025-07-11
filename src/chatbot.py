import os
import openai

def ask(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Send a prompt to the OpenAI API and return the assistant's response."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]


def main() -> None:
    prompt = input("You: ")
    answer = ask(prompt)
    print("Assistant:", answer)


if __name__ == "__main__":
    main()

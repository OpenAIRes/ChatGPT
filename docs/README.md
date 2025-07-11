# Documentation

This directory collects detailed guides for setting up and running the example chatbot.

## Setup

1. Install the required package:
   ```bash
   pip install openai
   ```
2. Export your OpenAI API key so the code can authenticate:
   ```bash
   export OPENAI_API_KEY=sk-<your-key>
   ```
3. (Optional) Run the test suite to confirm everything is configured correctly:
   ```bash
   python -m unittest discover tests
   ```

## Usage Example

Start an interactive session by running the chatbot module directly:

```bash
python -m src.chatbot
```

Each prompt you enter is sent to the API and the assistant responds. Submit an empty line at the `You:` prompt to end the conversation.

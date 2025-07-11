# Documentation

This directory collects detailed guides for setting up and running the example chatbot.

## Setup

1. Install the project locally using pip:
   ```bash
   pip install -e ..
   ```
   This command installs the `chatbot` console script along with the `openai` dependency.
2. Export your OpenAI API key so the code can authenticate:
   ```bash
   export OPENAI_API_KEY=sk-<your-key>
   ```
3. (Optional) Run the test suite to confirm everything is configured correctly:
   ```bash
   python -m unittest discover tests
   ```

## Usage Example

Start an interactive session by running the chatbot module directly. Command-line options let you configure the model, temperature, provide an initial system message, limit the response length, and store history in a file:

```bash
python -m src.chatbot [--model MODEL] [--temperature FLOAT] [--history-file PATH]
                         [--system-message TEXT] [--max-tokens INT]
```

Each prompt you enter is sent to the API and the assistant responds. Submit an empty line at the `You:` prompt to end the conversation.

## Logging

The example configures Python's built-in `logging` module. Adjust the verbosity
with the `LOG_LEVEL` environment variable:

```bash
LOG_LEVEL=DEBUG python -m src.chatbot
```

For larger applications consider using a dedicated logging framework like
`structlog` to emit structured logs.

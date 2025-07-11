# ChatGPT Repository

This repository contains a simple example project demonstrating how to integrate a chatbot using OpenAI's API. The goal of this repository is to provide a basic starting point for experimenting with ChatGPT-like functionality in your own projects.

## Goals

- Showcase how to send prompts to OpenAI's API and process responses.
- Provide example code that can be extended into a full-featured chatbot.
- Document setup steps and usage instructions.

## Directory Structure

- `src/` - application source code
- `tests/` - unit tests
- `docs/` - project documentation

## Getting Started

1. Install the project in editable mode:
   ```bash
   pip install -e .
   ```
   This installs the `chatbot` command and pulls in the required `openai` dependency.
2. Set your API key in the `OPENAI_API_KEY` environment variable.
3. Run the example script to interact with the chatbot: `python -m src.chatbot`.

## Running the Code

Once you have installed the dependencies and set your API key, start the chatbot interactively. You can optionally choose the model, adjust the temperature, and
store the conversation in a file. The session continues until you submit an empty line to exit:

```
python -m src.chatbot [--model MODEL] [--temperature FLOAT] [--history-file PATH]
```

Run the test suite to verify everything works as expected:

```
python -m unittest discover tests
```

## Contributing

Contributions are welcome! To contribute:

1. Fork this repository and create a new branch for your feature or fix.
2. Make your changes and commit them with clear messages.
3. Run the tests to ensure nothing is broken.
4. Open a pull request describing your changes.

## Contact

For questions or support, please open an issue on GitHub or email <open-source@example.com>.

## License

This project is released under the MIT License.

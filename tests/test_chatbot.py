import os
import sys
import types
import unittest

# Allow import from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Provide a minimal stub for the openai module so tests can run without the dependency
sys.modules.setdefault('openai', types.SimpleNamespace())

from src import chatbot


class ChatbotTests(unittest.TestCase):
    def test_missing_api_key(self):
        # Ensure the environment variable is absent
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        with self.assertRaises(EnvironmentError):
            chatbot.ask([{"role": "user", "content": "Hello"}])

    def test_empty_response(self):
        # Set API key so ask() proceeds
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        # Stub ChatCompletion.create to return an empty message
        class DummyResponse:
            def __init__(self):
                self.choices = [types.SimpleNamespace(message={"content": ""})]

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=lambda **_: DummyResponse())

        result = chatbot.ask([{"role": "user", "content": "Hi"}])
        self.assertEqual(result, "")

    def test_api_error(self):
        # Set API key so ask() proceeds
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        def raise_error(**_):
            raise RuntimeError("API error")

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=raise_error)

        with self.assertRaises(RuntimeError):
            chatbot.ask([{"role": "user", "content": "Hello"}])

    def test_max_tokens_argument(self):
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        captured: dict = {}

        def capture_call(**kwargs):
            captured.update(kwargs)

            class DummyResponse:
                def __init__(self):
                    self.choices = [types.SimpleNamespace(message={"content": "hi"})]

            return DummyResponse()

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=capture_call)

        chatbot.ask([{"role": "user", "content": "Hi"}], max_tokens=42)
        self.assertEqual(captured.get("max_tokens"), 42)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import types
import unittest
import logging

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



    def test_no_max_tokens_argument(self):
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        captured = {}

        def capture_call(**kwargs):
            captured.update(kwargs)

            class DummyResponse:
                def __init__(self):
                    self.choices = [types.SimpleNamespace(message={"content": "hi"})]

            return DummyResponse()

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=capture_call)

        chatbot.ask([{"role": "user", "content": "Hi"}])
        self.assertNotIn("max_tokens", captured)

    def test_multiple_choices(self):
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        class DummyResponse:
            def __init__(self):
                self.choices = [
                    types.SimpleNamespace(message={"content": "first"}),
                    types.SimpleNamespace(message={"content": "second"}),
                ]

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=lambda **_: DummyResponse())

        result = chatbot.ask([{"role": "user", "content": "Hi"}])
        self.assertEqual(result, "first")

    def test_no_choices_in_response(self):
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        class DummyResponse:
            def __init__(self):
                self.choices = []

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=lambda **_: DummyResponse())

        with self.assertRaises(IndexError):
            chatbot.ask([{"role": "user", "content": "Hi"}])

    def test_default_arguments(self):
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        captured = {}

        def capture_call(**kwargs):
            captured.update(kwargs)

            class DummyResponse:
                def __init__(self):
                    self.choices = [types.SimpleNamespace(message={"content": "ok"})]

            return DummyResponse()

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=capture_call)

        chatbot.ask([{"role": "user", "content": "Hi"}])

        self.assertEqual(captured.get("model"), "gpt-3.5-turbo")
        self.assertEqual(captured.get("temperature"), 0.7)

    def test_custom_arguments(self):
        os.environ["OPENAI_API_KEY"] = "dummy-key"

        captured = {}

        def capture_call(**kwargs):
            captured.update(kwargs)

            class DummyResponse:
                def __init__(self):
                    self.choices = [types.SimpleNamespace(message={"content": "ok"})]

            return DummyResponse()

        openai = sys.modules['openai']
        openai.ChatCompletion = types.SimpleNamespace(create=capture_call)

        chatbot.ask(
            [{"role": "user", "content": "Hi"}],
            model="gpt-custom",
            temperature=0.3,
        )

        self.assertEqual(captured.get("model"), "gpt-custom")
        self.assertEqual(captured.get("temperature"), 0.3)

    def test_configure_logging_debug_level(self):
        # Remove any existing handlers so basicConfig has an effect
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
        root_logger.setLevel(logging.NOTSET)

        chatbot.configure_logging("debug")

        self.assertEqual(root_logger.level, logging.DEBUG)


if __name__ == "__main__":
    unittest.main()

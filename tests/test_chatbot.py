import os
import sys
import unittest

# Allow import from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import chatbot


class ChatbotTests(unittest.TestCase):
    def test_missing_api_key(self):
        # Ensure the environment variable is absent
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        with self.assertRaises(EnvironmentError):
            chatbot.ask("Hello")


if __name__ == "__main__":
    unittest.main()

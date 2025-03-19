# tests/llm/test_auto_bundle.py

# TODO convert to pytest
import unittest

from unittest.mock import AsyncMock, patch

from filebundler.lib.llm.utils import AnthropicModelName
from filebundler.lib.llm.auto_bundle import prompt_llm, AutoBundleResponse


class TestAutoBundleUtil(unittest.TestCase):
    @patch("filebundler.lib.llm.auto_bundle.Agent")
    @patch("filebundler.lib.llm.auto_bundle.AnthropicModel")
    async def test_prompt_llm(self, mock_anthropic_model, mock_agent):
        # Setup test data
        model_type = AnthropicModelName.CLAUDE_HAIKU
        user_prompt = "Help me find files related to authentication"
        file_contents = "Sample file content"

        # Mock the response
        mock_response = AutoBundleResponse(
            name="auth-files",
            files={
                "very_likely_useful": ["auth.py", "login.py"],
                "probably_useful": ["user.py"],
            },
            message="These files contain authentication logic",
        )

        # Set up the mock agent
        mock_agent_instance = AsyncMock()
        mock_agent_instance.run.return_value = mock_response
        mock_agent.return_value = mock_agent_instance

        # Call the function
        result = await prompt_llm(
            model_type=model_type, user_prompt=user_prompt, file_contents=file_contents
        )

        # Verify calls
        mock_anthropic_model.assert_called_once_with(model_type.value, api_key=None)
        mock_agent.assert_called_once()
        mock_agent_instance.run.assert_called_once()

        # Verify response
        self.assertEqual(result, mock_response)
        self.assertEqual(result.name, "auth-files")
        self.assertEqual(len(result.files["very_likely_useful"]), 2)
        self.assertEqual(len(result.files["probably_useful"]), 1)
        self.assertEqual(result.message, "These files contain authentication logic")


if __name__ == "__main__":
    unittest.main()

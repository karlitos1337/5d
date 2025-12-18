
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.github_oauth import GitHubAuth

class TestGitHubOAuthSecurity(unittest.TestCase):
    def setUp(self):
        # Setup environment variables required by GitHubAuth
        self.env_patcher = patch.dict(os.environ, {
            "GITHUB_CLIENT_ID": "test_id",
            "GITHUB_CLIENT_SECRET": "test_secret"
        })
        self.env_patcher.start()
        self.auth = GitHubAuth()

    def tearDown(self):
        self.env_patcher.stop()

    @patch("requests.post")
    def test_exchange_code_for_token_timeout(self, mock_post):
        """Test that exchange_code_for_token uses a timeout."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "token"}
        mock_post.return_value = mock_response

        self.auth.exchange_code_for_token("test_code")

        # Verify call args include timeout
        args, kwargs = mock_post.call_args
        self.assertIn("timeout", kwargs, "requests.post should be called with a timeout")
        self.assertEqual(kwargs["timeout"], 10, "Timeout should be 10 seconds")

    @patch("requests.get")
    def test_verify_user_exists_timeout(self, mock_get):
        """Test that verify_user_exists uses a timeout."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        self.auth.verify_user_exists("test_token")

        # Verify call args include timeout
        args, kwargs = mock_get.call_args
        self.assertIn("timeout", kwargs, "requests.get should be called with a timeout")
        self.assertEqual(kwargs["timeout"], 10, "Timeout should be 10 seconds")

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from auth.github_oauth import GitHubAuth
import os

class TestGitHubOAuthSecurity(unittest.TestCase):
    @patch.dict(os.environ, {"GITHUB_CLIENT_ID": "test_id", "GITHUB_CLIENT_SECRET": "test_secret"})
    def setUp(self):
        self.auth = GitHubAuth()

    @patch('requests.post')
    def test_exchange_code_for_token_timeout(self, mock_post):
        """Test that requests.post is called with a timeout."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "token"}
        mock_post.return_value = mock_response

        # Call the method
        self.auth.exchange_code_for_token("test_code")

        # Verify timeout is present
        args, kwargs = mock_post.call_args
        self.assertIn('timeout', kwargs, "Security Risk: requests.post missing timeout")
        self.assertGreater(kwargs['timeout'], 0, "Timeout must be positive")

    @patch('requests.get')
    def test_verify_user_exists_timeout(self, mock_get):
        """Test that requests.get is called with a timeout."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call method
        self.auth.verify_user_exists("token")

        # Verify timeout is present
        args, kwargs = mock_get.call_args
        self.assertIn('timeout', kwargs, "Security Risk: requests.get missing timeout")

if __name__ == '__main__':
    unittest.main()

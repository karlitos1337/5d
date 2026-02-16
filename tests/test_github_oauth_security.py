import os
import unittest
from unittest.mock import patch

from auth.github_oauth import GitHubAuth


class TestGitHubOAuthSecurity(unittest.TestCase):
    def setUp(self):
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.redirect_uri = "http://localhost:8501"
        with patch.dict(os.environ, {
            "GITHUB_CLIENT_ID": self.client_id,
            "GITHUB_CLIENT_SECRET": self.client_secret,
            "GITHUB_REDIRECT_URI": self.redirect_uri
        }):
            self.auth = GitHubAuth()

    def test_environment_variable_loading(self):
        """Verify that credentials are loaded from environment variables (mocked), not hardcoded."""
        self.assertEqual(self.auth.client_id, self.client_id)
        self.assertEqual(self.auth.client_secret, self.client_secret)
        self.assertEqual(self.auth.redirect_uri, self.redirect_uri)

    def test_auth_url_construction(self):
        """Verify the auth URL is constructed correctly."""
        expected_url = f"https://github.com/login/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=user"
        self.assertEqual(self.auth.get_auth_url(), expected_url)

    @patch("requests.post")
    def test_get_access_token_security(self, mock_post):
        """Verify that the access token request uses the secret securely (passed in body, not URL query if possible, though standard OAuth uses body)."""
        mock_post.return_value.json.return_value = {"access_token": "mock_token"}

        token = self.auth.get_access_token("mock_code")

        self.assertEqual(token, "mock_token")
        mock_post.assert_called_once()

        # Check that client_secret is in the payload
        args, kwargs = mock_post.call_args
        self.assertIn("data", kwargs)
        self.assertEqual(kwargs["data"]["client_secret"], self.client_secret)

if __name__ == "__main__":
    unittest.main()

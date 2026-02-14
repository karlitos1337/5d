import unittest
from unittest.mock import patch
import os
from urllib.parse import parse_qs, urlparse
from auth.github_oauth import GitHubAuth

class TestGitHubOAuthSecurity(unittest.TestCase):
    def setUp(self):
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.redirect_uri = "http://localhost:8501"

        # Patch environment variables for GitHubAuth
        self.env_patcher = patch.dict(os.environ, {
            "GITHUB_CLIENT_ID": self.client_id,
            "GITHUB_CLIENT_SECRET": self.client_secret,
            "GITHUB_REDIRECT_URI": self.redirect_uri
        })
        self.env_patcher.start()

        self.auth = GitHubAuth()

    def tearDown(self):
        self.env_patcher.stop()

    def test_state_generation_and_validation(self):
        """Verify that state parameter is generated randomly and validated correctly."""
        # 1. Generate Authorization URL
        auth_url, state = self.auth.get_authorization_url()

        # Check URL structure
        parsed_url = urlparse(auth_url)
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "github.com")
        self.assertEqual(parsed_url.path, "/login/oauth/authorize")

        # Check params
        params = parse_qs(parsed_url.query)
        self.assertEqual(params["client_id"][0], self.client_id)
        self.assertEqual(params["redirect_uri"][0], self.redirect_uri)
        self.assertIn("state", params)
        self.assertEqual(params["state"][0], state)

        # Verify randomness (simple check)
        auth_url2, state2 = self.auth.get_authorization_url()
        self.assertNotEqual(state, state2)

    @patch("requests.post")
    @patch("requests.get")
    def test_token_exchange_success(self, mock_get, mock_post):
        """Test successful token exchange."""
        # Mock Token Response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "access_token": "gho_test_token",
            "token_type": "bearer",
            "scope": "read:user"
        }

        # Mock User Info Response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "login": "testuser",
            "id": 12345,
            "email": "test@example.com"
        }

        # Mocking verify_user_exists to rely on our mocked get
        # But exchange_code_for_token calls requests.post, and verify calls requests.get

        # We need to simulate the flow manually or trust authenticate method?
        # Let's test authenticate method directly

        result = self.auth.authenticate("test_code", "state123", "state123")

        self.assertIsNotNone(result)
        self.assertIn("session_token", result)

    @patch("requests.post")
    def test_token_exchange_failure(self, mock_post):
        """Test handling of token exchange failure."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "error": "bad_verification_code",
            "error_description": "The code passed is incorrect or expired."
        }

        # authenticate calls exchange_code_for_token
        result = self.auth.authenticate("invalid_code", "state123", "state123")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()

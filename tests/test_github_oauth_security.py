import unittest
from unittest.mock import patch
import os

from urllib.parse import parse_qs, urlparse
from auth.github_oauth import GitHubAuth


class TestGitHubOAuthSecurity(unittest.TestCase):
    def setUp(self):
        # Setup environment variables
        self.env_patcher = patch.dict(
            os.environ,
            {
                "GITHUB_CLIENT_ID": "test_client_id",
                "GITHUB_CLIENT_SECRET": "test_client_secret",
                "GITHUB_REDIRECT_URI": "http://localhost:8000/callback",
            },
        )
        self.env_patcher.start()
        self.auth = GitHubAuth()

    def tearDown(self):
        self.env_patcher.stop()

    def test_get_authorization_url_secure_encoding(self):
        """Test that authorization URL is correctly encoded and returns state."""
        url, state = self.auth.get_authorization_url()

        # Verify URL structure
        parsed_url = urlparse(url)
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "github.com")
        self.assertEqual(parsed_url.path, "/login/oauth/authorize")

        # Verify query parameters
        params = parse_qs(parsed_url.query)
        self.assertEqual(params["client_id"][0], "test_client_id")
        self.assertEqual(params["redirect_uri"][0], "http://localhost:8000/callback")
        self.assertEqual(params["state"][0], state)

        # Verify state is strong random
        self.assertEqual(len(state), 43)  # 32 bytes base64url encoded is approx 43 chars

    def test_get_authorization_url_custom_state(self):
        """Test with custom state."""
        custom_state = "custom_secure_state"
        url, state = self.auth.get_authorization_url(state=custom_state)
        self.assertEqual(state, custom_state)
        self.assertIn(f"state={custom_state}", url)

    @patch("auth.github_oauth.requests.post")
    @patch("auth.github_oauth.requests.get")
    def test_authenticate_success(self, mock_get, mock_post):
        """Test successful authentication flow with valid state."""
        # Mock responses
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "valid_token"}

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"login": "testuser"}

        state = "valid_state"
        code = "valid_code"

        result = self.auth.authenticate(code, received_state=state, expected_state=state)

        self.assertIsNotNone(result)
        self.assertIn("session_token", result)

        # Verify calls
        mock_post.assert_called_with(
            "https://github.com/login/oauth/access_token",
            json={
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
                "code": code,
                "redirect_uri": "http://localhost:8000/callback",
            },
            headers={"Accept": "application/json"},
            timeout=10,  # Security check: timeout must be present
        )

    def test_authenticate_csrf_mismatch(self):
        """Test that authentication fails when states do not match."""
        result = self.auth.authenticate(
            "code", received_state="bad_state", expected_state="good_state"
        )
        self.assertIsNone(result)

    def test_authenticate_missing_state(self):
        """Test that authentication fails when state is missing."""
        result = self.auth.authenticate("code", received_state="", expected_state="good_state")
        self.assertIsNone(result)

        result = self.auth.authenticate("code", received_state="good_state", expected_state=None)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

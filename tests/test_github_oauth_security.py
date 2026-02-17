import os
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from auth.github_oauth import GitHubAuth


class TestGitHubOAuthSecurity(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.redirect_uri = "http://localhost:8501"

        # Patch environment variables
        self.env_patcher = patch.dict(
            os.environ,
            {
                "GITHUB_CLIENT_ID": self.client_id,
                "GITHUB_CLIENT_SECRET": self.client_secret,
                "REDIRECT_URI": self.redirect_uri,
            },
        )
        self.env_patcher.start()

        self.auth = GitHubAuth()

    def tearDown(self):
        """Tear down test fixtures."""
        self.env_patcher.stop()

    def test_get_auth_url_contains_state(self):
        """Test that the authorization URL contains a random state parameter."""
        # Update: get_auth_url was renamed to get_authorization_url in GitHubAuth
        auth_url, state = self.auth.get_authorization_url()
        parsed_url = urlparse(auth_url)
        params = parse_qs(parsed_url.query)

        self.assertIn("state", params)
        self.assertEqual(params["state"][0], state)
        self.assertTrue(len(state) > 0)

    # Note: Removed test_get_auth_url_stores_state as GitHubAuth is designed to be stateless
    # regarding session storage (it returns state, caller handles storage).
    # The previous test mocked 'st' which isn't present in GitHubAuth class anymore.


if __name__ == "__main__":
    unittest.main()

import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO

# Add web/5d-map to path so we can import owid_proxy
sys.path.append(os.path.join(os.path.dirname(__file__), "../web/5d-map"))

import owid_proxy  # type: ignore

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        self.mock_request = MagicMock()
        self.mock_client_address = ("127.0.0.1", 12345)
        self.mock_server = MagicMock()

        # Instantiate handler without calling __init__ (which triggers handle())
        # because BaseHTTPRequestHandler calls handle() in __init__
        self.handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        self.handler.request = self.mock_request
        self.handler.client_address = self.mock_client_address
        self.handler.server = self.mock_server
        self.handler.wfile = BytesIO()
        self.handler.rfile = BytesIO()
        # Required for log_request to work without crashing if called
        self.handler.requestline = "GET /proxy/test.csv HTTP/1.1"

        # We need to set up the path for the handler manually since we skipped __init__
        self.handler.path = "/proxy/depression-prevalence.csv"
        self.handler.command = "GET"
        self.handler.request_version = "HTTP/1.1"
        self.handler.protocol_version = "HTTP/1.1"

    @patch("urllib.request.urlopen")
    def test_dos_protection_large_response(self, mock_urlopen):
        """Test that the proxy aborts if the response is too large."""
        # Mock a response that returns a huge amount of data
        mock_response = MagicMock()
        # Simulate a stream that keeps giving data
        # We want it to exceed the limit (which we will set to 10MB)
        # Let's mock the 'read' method to return 1MB chunks
        chunk = b"A" * (1024 * 1024) # 1MB

        # Returns 11 chunks of 1MB (11MB total) then empty bytes
        mock_response.read.side_effect = [chunk] * 11 + [b""]
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        # Execute GET
        self.handler.do_GET()

        response = self.handler.wfile.getvalue()

        # We expect a 502 Bad Gateway or similar, with a specific error
        # Currently the code just crashes or writes everything.
        # After our fix, it should write an error message.

        # For now (before fix), this test would likely fail or hang if we didn't limit the read side_effect
        # But we want to assert that it handles it gracefully.

        # Check if the output contains "Response too large" (which we plan to add)
        # or just check status code if we can parse it from wfile

        self.assertIn(b"Response too large", response)

    @patch("urllib.request.urlopen")
    def test_error_leakage_sanitization(self, mock_urlopen):
        """Test that internal error details are not leaked to the client."""
        # Mock an exception with sensitive info
        mock_urlopen.side_effect = Exception("SENSITIVE_DB_CONNECTION_STRING_FAILED")

        self.handler.do_GET()

        response = self.handler.wfile.getvalue()

        # Should contain generic error
        self.assertIn(b"Fetch error", response)

        # Should NOT contain sensitive info
        self.assertNotIn(b"SENSITIVE_DB_CONNECTION_STRING_FAILED", response)

    @patch("urllib.request.urlopen")
    def test_security_headers(self, mock_urlopen):
        """Test that security headers are present."""
        mock_response = MagicMock()
        mock_response.read.side_effect = [b"csv,data", b""]
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        self.handler.do_GET()

        response = self.handler.wfile.getvalue().decode()

        # Check for X-Content-Type-Options: nosniff
        self.assertIn("X-Content-Type-Options: nosniff", response)

if __name__ == "__main__":
    unittest.main()

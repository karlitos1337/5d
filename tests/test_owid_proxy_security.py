import importlib.util
import sys
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

# Load owid_proxy module dynamically
spec = importlib.util.spec_from_file_location("owid_proxy", "web/5d-map/owid_proxy.py")
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)


class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        self.client_address = ("127.0.0.1", 12345)
        self.server = MagicMock()

    def create_handler(self, path):
        self.wfile = BytesIO()

        # Create a partial mock instance bypassing __init__
        handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        handler.client_address = self.client_address
        handler.requestline = f"GET /{path} HTTP/1.1"
        handler.command = "GET"
        handler.path = f"/{path}"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = self.wfile
        handler.server = self.server
        handler.protocol_version = "HTTP/1.1"

        # Mock send_response and send_header to write to wfile for inspection
        # But BaseHTTPRequestHandler writes to wfile anyway.
        # However, we need to initialize headers_buffer or similar if we use original methods.
        # To avoid complexity of BaseHTTPRequestHandler internals, we rely on it writing to wfile.
        # We just need to make sure basic attributes are set.

        # Initialize internal structures needed by send_response/send_header
        handler._headers_buffer = []

        return handler

    @patch("urllib.request.urlopen")
    def test_dos_protection_max_size(self, mock_urlopen):
        """Test that the proxy rejects responses larger than MAX_RESPONSE_SIZE"""
        # Create content slightly larger than 10MB
        # We don't need to actually create 10MB string if we mock read chunking behavior,
        # but to be safe and simple, let's just make it check the logic.

        # Mock response object
        mock_resp = MagicMock()

        # We simulate a stream that returns chunks
        # Total size > 10MB (10 * 1024 * 1024)
        chunk_size = 1024 * 1024  # 1MB
        chunks = [b"A" * chunk_size] * 11  # 11 chunks = 11MB

        # Iterator for side_effect
        chunk_iter = iter(chunks)

        def side_effect_read(n=-1):
            try:
                if n == -1:
                    # If code calls read(), it gets everything (VULNERABLE PATH)
                    return b"".join(chunks)
                return next(chunk_iter)
            except StopIteration:
                return b""

        mock_resp.read.side_effect = side_effect_read
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        handler = self.create_handler("proxy/depression-prevalence.csv")

        # Run handler
        handler.do_GET()

        output = self.wfile.getvalue()

        # Check for failure
        # In the vulnerable version, it will try to read all and succeed (returning 200 OK)
        # In the fixed version, it should stop early and return error

        # If the code is fixed, we expect a 502 or 413 or generic error.
        # And importantly, we expect it NOT to output the full content.

        # In the vulnerable version, it returns 200 OK.
        # We want to ensure it DOES NOT return 200 OK for oversized content.
        if b"200 OK" in output:
            # If we are strictly TDD, we might assertFail here, but since we are modifying the code
            # let's just assert that we WANT an error.
            # However, for the reproduction step, we acknowledge it currently passes (vulnerable).
            # I'll force a failure if it's 200 OK to confirm vulnerability.
            self.fail("Vulnerability confirmed: Proxy accepted oversized response (DoS risk)")

        self.assertIn(b"Response too large", output)

    @patch("urllib.request.urlopen")
    def test_error_sanitization(self, mock_urlopen):
        """Test that internal error details are not leaked"""
        # Mock an error with sensitive info
        sensitive_info = "Database connection failed at 192.168.1.5:5432"
        mock_urlopen.side_effect = Exception(sensitive_info)

        handler = self.create_handler("proxy/depression-prevalence.csv")
        handler.do_GET()

        output = self.wfile.getvalue()

        # Should NOT contain the sensitive info
        self.assertNotIn(sensitive_info.encode(), output)
        # Should contain generic error
        self.assertIn(b"Fetch error", output)

    @patch("urllib.request.urlopen")
    def test_security_headers(self, mock_urlopen):
        """Test that security headers are present"""
        mock_resp = MagicMock()
        # Ensure read returns data once then EOF
        mock_resp.read.side_effect = [b"csv,data", b""]
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        handler = self.create_handler("proxy/depression-prevalence.csv")
        handler.do_GET()

        output = self.wfile.getvalue()

        self.assertIn(b"X-Content-Type-Options: nosniff", output)


if __name__ == "__main__":
    unittest.main()

import importlib.util
import io
import sys
import unittest
from unittest.mock import MagicMock, patch

# Load the owid_proxy module dynamically
PROXY_PATH = "web/5d-map/owid_proxy.py"
spec = importlib.util.spec_from_file_location("owid_proxy", PROXY_PATH)
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)

class TestHandler(owid_proxy.ProxyHandler):
    """Subclass to bypass BaseHTTPRequestHandler.__init__ and capture output."""
    def __init__(self):
        self.path = ""
        self.wfile = io.BytesIO()
        self.headers_buffer = {}
        self.response_code = 0
        # Mocking rfile just in case, though do_GET shouldn't read it
        self.rfile = io.BytesIO()

    def send_header(self, k, v):
        self.headers_buffer[k] = v

    def send_response(self, code, message=None):
        self.response_code = code

    def end_headers(self):
        pass

    def log_message(self, fmt, *args):
        pass

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        self.handler = TestHandler()

    @patch('urllib.request.urlopen')
    def test_security_headers_present(self, mock_urlopen):
        """Verify X-Content-Type-Options: nosniff is set."""
        self.handler.path = "/proxy/depression-prevalence.csv"

        # Mock successful response
        mock_resp = MagicMock()
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.__exit__.return_value = None
        mock_resp.read.side_effect = [b"Code,Year,Val\nABC,2020,10", b""] # Chunked
        mock_urlopen.return_value = mock_resp

        self.handler.do_GET()

        self.assertEqual(self.handler.response_code, 200)
        self.assertEqual(self.handler.headers_buffer.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(self.handler.headers_buffer.get("Access-Control-Allow-Origin"), "*")

    @patch('urllib.request.urlopen')
    def test_max_response_size_limit(self, mock_urlopen):
        """Verify that responses larger than limit are rejected."""
        self.handler.path = "/proxy/depression-prevalence.csv"

        # Mock huge response (larger than 10MB)
        # We simulate a loop of chunks
        chunk_size = 1024 * 1024 # 1MB
        chunks = [b"x" * chunk_size] * 11 # 11MB total
        chunks.append(b"")

        mock_resp = MagicMock()
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.__exit__.return_value = None
        mock_resp.read.side_effect = chunks
        mock_urlopen.return_value = mock_resp

        # Capture print output to verify internal logging if possible,
        # but mainly check that it stops and doesn't crash or return full data
        with patch('builtins.print'):
            self.handler.do_GET()

            # Should not crash, and should probably not write all 11MB to wfile if we implement abort
            # Note: The current implementation (before fix) will write all 11MB.
            # The test expects the FIX behavior (aborting).
            # If this test runs BEFORE fix, it might fail or pass depending on assertion.

            # After fix, it should stop writing.
            # We can check if wfile size is < 11MB or if it logged an error.
            self.assertTrue(len(self.handler.wfile.getvalue()) < 11 * 1024 * 1024)

    @patch('urllib.request.urlopen')
    def test_error_sanitization(self, mock_urlopen):
        """Verify that 502 errors do not leak exception details."""
        self.handler.path = "/proxy/depression-prevalence.csv"

        # Mock exception with sensitive info
        mock_urlopen.side_effect = Exception("SENSITIVE_DB_INFO_LEAK")

        self.handler.do_GET()

        self.assertEqual(self.handler.response_code, 502)
        self.assertEqual(self.handler.headers_buffer.get("X-Content-Type-Options"), "nosniff")

        body = self.handler.wfile.getvalue().decode('utf-8')
        self.assertNotIn("SENSITIVE_DB_INFO_LEAK", body)
        self.assertIn("Upstream fetch error", body)

if __name__ == "__main__":
    unittest.main()

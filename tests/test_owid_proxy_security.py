import unittest
import importlib.util
import sys
import io
from unittest.mock import MagicMock, patch

# Load the owid_proxy module dynamically
PROXY_PATH = "web/5d-map/owid_proxy.py"
spec = importlib.util.spec_from_file_location("owid_proxy", PROXY_PATH)
from unittest.mock import MagicMock, patch
import sys
import os
import importlib.util
from io import BytesIO

# Load the module dynamically
file_path = os.path.join("web", "5d-map", "owid_proxy.py")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Could not find {file_path}")

spec = importlib.util.spec_from_file_location("owid_proxy", file_path)
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
class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        self.mock_wfile = BytesIO()
        self.mock_wfile.close = lambda: None # Prevent closing

        # Create a mock handler without invoking __init__ which requires a real socket
        self.handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        self.handler.client_address = ('127.0.0.1', 5510)
        self.handler.request_version = 'HTTP/1.1'
        self.handler.server_version = 'BaseHTTP/0.6'
        self.handler.sys_version = 'Python/3.x'
        self.handler.wfile = self.mock_wfile
        self.handler.rfile = BytesIO()
        self.handler.headers = {}

        # Manually set up things usually done in __init__
        self.handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"
        self.handler.path = "/proxy/depression-prevalence.csv"
        self.handler.command = "GET"

        # Mock send_header and end_headers to capture output better if needed
        # But BaseHTTPRequestHandler writes to wfile, so we can check that.

    @patch('urllib.request.urlopen')
    def test_no_stack_trace_leak(self, mock_urlopen):
        """Test that exception details are not leaked to the client."""
        # Simulate a crash with a sensitive message
        sensitive_info = "SENSITIVE_DB_PASSWORD_123"
        mock_urlopen.side_effect = Exception(f"Connection failed: {sensitive_info}")

        self.handler.do_GET()

        response = self.mock_wfile.getvalue().decode('utf-8', errors='ignore')

        # Check that we got a 502
        self.assertIn("502 Bad Gateway", response) # BaseHTTPRequestHandler might write status line differently depending on python version, but usually logs it.
        # Actually send_response writes "HTTP/1.0 502 Bad Gateway\r\n"

        # CRITICAL: The sensitive info must NOT be in the response
        self.assertNotIn(sensitive_info, response, "Sensitive exception details leaked in error response!")
        self.assertIn("Fetch error", response) # Current behavior (should fail if I change it later, but for now verifying fail)

    @patch('urllib.request.urlopen')
    def test_security_headers(self, mock_urlopen):
        """Test that security headers are present."""
        mock_resp = MagicMock()
        mock_resp.read.side_effect = [b"csv,data", b""]
        mock_resp.__enter__.return_value = mock_resp
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
        with patch('builtins.print') as mock_print:
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
        response = self.mock_wfile.getvalue().decode('utf-8')

        self.assertIn("HTTP/1.0 200 OK", response)
        self.assertIn("X-Content-Type-Options: nosniff", response, "Missing X-Content-Type-Options header")

    @patch('urllib.request.urlopen')
    def test_large_response_dos(self, mock_urlopen):
        """Test that the server enforces a size limit."""
        # Create a mock that returns a huge amount of data
        # If the code uses resp.read(), it will consume all of it.
        # If the code uses chunked read with limit, it should stop early.

        MAX_TEST_LIMIT = 10 * 1024 * 1024 + 100 # Just over 10MB

        # We simulate a stream that yields chunks
        class MockStreamResponse:
            def __init__(self):
                self.read_count = 0

            def read(self, size=-1):
                # If size is -1 (default), it reads everything -> Bad!
                if size == -1:
                    return b"A" * MAX_TEST_LIMIT

                # If chunked, return chunks
                if self.read_count >= MAX_TEST_LIMIT:
                     return b"" # End of stream

                self.read_count += size
                return b"A" * size

            def __enter__(self): return self
            def __exit__(self, *args): pass

        mock_urlopen.return_value = MockStreamResponse()

        # We want to check if the implementation calls read() without args (unbounded) or with args.
        # However, we can't easily spy on the method call if we replace the object.
        # So we'll use a Spy or check side effects.

        # Let's verify that the response written to wfile is NOT the full size if we enforce a limit.
        # OR we can check that it raises an error.

        # Current implementation: read() consumes everything.
        # We expect this test to fail because currently it reads everything (mock returns MAX_TEST_LIMIT bytes).

        self.handler.do_GET()

        response_body = self.mock_wfile.getvalue()
        # Extract body (after headers)
        body_start = response_body.find(b"\r\n\r\n") + 4
        body = response_body[body_start:]

        # If vulnerability exists, body will be huge
        # If fixed, body should be error message or truncated

        self.assertLess(len(body), 10 * 1024 * 1024, "Response size exceeded 10MB limit! DoS risk.")

if __name__ == '__main__':
    unittest.main()

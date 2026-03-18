import importlib.util
import io
import os
import unittest
from unittest.mock import patch

# Load owid_proxy dynamically
PROXY_PATH = os.path.join(os.getcwd(), 'web/5d-map/owid_proxy.py')
spec = importlib.util.spec_from_file_location("owid_proxy", PROXY_PATH)
owid_proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owid_proxy)

class MockStreamResponse:
    def __init__(self, data=b""):
        self.data = data
        self.position = 0
        self.closed = False

    def read(self, size=-1):
        if self.closed:
            raise ValueError("I/O operation on closed file")
        if size == -1 or size is None:
            ret = self.data[self.position:]
            self.position = len(self.data)
            return ret
        else:
            end = min(self.position + size, len(self.data))
            ret = self.data[self.position:end]
            self.position = end
            return ret

    def close(self):
        self.closed = True

    def getheader(self, name):
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        # We subclass to bypass __init__ and its socket binding attempts
        class TestableHandler(owid_proxy.ProxyHandler):
            def __init__(self):
                self.rfile = io.BytesIO()
                self.wfile = io.BytesIO()
                # Mock attributes needed by BaseHTTPRequestHandler
                self.request_version = "HTTP/1.1"
                self.sys_version = "Python/3"
                self.server_version = "TestServer"
                self.path = "/proxy/depression-prevalence.csv"
                self.headers = {}
                self.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"
                self.client_address = ('127.0.0.1', 12345)

                # Mock wfile.close to prevent early closing
                self._original_close = self.wfile.close
                self.wfile.close = lambda: None

        self.handler_class = TestableHandler

    def test_security_headers_present(self):
        handler = self.handler_class()

        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value = MockStreamResponse(b"test data")
            handler.do_GET()

        output = handler.wfile.getvalue().decode('utf-8', errors='ignore')
        # Verify status 200
        self.assertTrue("200 OK" in output, "Expected 200 OK response")
        # Verify header
        self.assertIn("X-Content-Type-Options: nosniff", output)

    def test_error_sanitization(self):
        handler = self.handler_class()

        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.side_effect = Exception("SensitiveInternalDetails_DB_FAIL")
            handler.do_GET()

        output = handler.wfile.getvalue().decode('utf-8', errors='ignore')
        # Should be 502
        self.assertTrue("502" in output, "Expected 502 response")
        # Should NOT contain sensitive detail
        self.assertNotIn("SensitiveInternalDetails", output)
        # Should contain generic error
        self.assertIn("Upstream service unavailable", output)

    def test_response_size_limit(self):
        handler = self.handler_class()

        # Create a huge response > 10MB
        large_data = b"x" * (10 * 1024 * 1024 + 100) # 10MB + 100 bytes

        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value = MockStreamResponse(large_data)
            handler.do_GET()

        output = handler.wfile.getvalue().decode('utf-8', errors='ignore')

        # We expect it to fail with 502 and specific message
        self.assertTrue("502" in output, "Expected 502 response")
        self.assertIn("Response too large", output)

import sys
import unittest
from unittest.mock import MagicMock, patch

# Load the owid_proxy module dynamically
PROXY_PATH = "web/5d-map/owid_proxy.py"
spec = importlib.util.spec_from_file_location("owid_proxy", PROXY_PATH)
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)

if __name__ == '__main__':
    unittest.main()

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
        mock_resp.getheader.return_value = "100"
        mock_resp.read.side_effect = [b"Code,Year,Val\nABC,2020,10", b""] * 10 # Provide enough items for multiple reads
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

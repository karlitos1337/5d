import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import io
import importlib.util

# Load the module dynamically
file_path = os.path.join(os.getcwd(), 'web/5d-map/owid_proxy.py')
spec = importlib.util.spec_from_file_location("owid_proxy", file_path)
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)

class MockStreamResponse:
    def __init__(self, data_size):
        self.data_size = data_size
        self.read_so_far = 0

    def read(self, size=None):
        # Simulate infinite/large stream
        if size is None:
            # Legacy behavior: read all
            return b'x' * self.data_size

        if self.read_so_far >= self.data_size:
            return b''

        to_read = min(size, self.data_size - self.read_so_far)
        self.read_so_far += to_read
        return b'x' * to_read

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

class TestOwidProxySecurity(unittest.TestCase):

    def setUp(self):
        pass

    def _get_handler(self, path):
        handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        handler.path = path
        handler.wfile = io.BytesIO()
        handler.request_version = "HTTP/1.1"
        handler.server_version = "BaseHTTP/0.6"
        handler.sys_version = ""
        handler.command = "GET"
        handler.requestline = f"GET {path} HTTP/1.1"
        handler.client_address = ('127.0.0.1', 5555)

        # Mock send_response/send_header to write to wfile for easier parsing (or just rely on wfile)
        # BaseHTTPRequestHandler writes headers to wfile.
        # But we need to make sure headers_buffer is initialized if we bypassed __init__?
        # Actually BaseHTTPRequestHandler doesn't use headers_buffer in older python?
        # In Python 3, it writes to wfile directly or buffers.
        # Let's verify if bypass __init__ causes issues.
        # It initializes self.headers to None? No, it doesn't use self.headers for writing.
        # But send_response calls log_request which might fail if we don't mock it or set attributes.
        # I set requestline/client_address so log_request should be fine.

        return handler

    @patch('urllib.request.urlopen')
    def test_missing_security_headers(self, mock_urlopen):
        # Setup mock
        mock_stream = MockStreamResponse(100) # Small response
        mock_urlopen.return_value = mock_stream

        handler = self._get_handler("/proxy/depression-prevalence.csv")
        handler.do_GET()

        output = handler.wfile.getvalue().decode('latin-1')

        # Verify status 200
        self.assertIn("200 OK", output)

        # CHECK 1: X-Content-Type-Options (Expect Failure on current code)
        if "X-Content-Type-Options: nosniff" not in output:
            self.fail("SECURITY VULNERABILITY: X-Content-Type-Options header missing")

    @patch('urllib.request.urlopen')
    def test_response_size_limit(self, mock_urlopen):
        # Setup mock with 11MB data (limit should be 10MB)
        # We use a smaller chunks but total size > 10MB
        large_size = 11 * 1024 * 1024
        mock_stream = MockStreamResponse(large_size)
        mock_urlopen.return_value = mock_stream

        handler = self._get_handler("/proxy/depression-prevalence.csv")
        handler.do_GET()

        output = handler.wfile.getvalue().decode('latin-1')

        # CHECK 2: Size Limit (Expect Failure on current code)
        # If vulnerable, it returns 200 and the full data (or at least starts sending it)
        # If fixed, it should probably return 502 or 413, or at least NOT 200 OK with full data.

        # Current behavior: 200 OK.
        # Desired behavior: Error response.

        if "200 OK" in output:
             self.fail("SECURITY VULNERABILITY: Large response was accepted (DoS risk)")

    @patch('urllib.request.urlopen')
    def test_error_message_leakage(self, mock_urlopen):
        # Setup mock to raise exception with sensitive info
        sensitive_info = "ConnectionRefusedError: [Errno 111] InternalDB:3306"
        mock_urlopen.side_effect = Exception(sensitive_info)

        handler = self._get_handler("/proxy/depression-prevalence.csv")
        handler.do_GET()

        output = handler.wfile.getvalue().decode('latin-1')

        # Verify 502
        self.assertIn("502 Bad Gateway", output) # Or whatever the code sends

        # CHECK 3: Leakage (Expect Failure on current code)
        if sensitive_info in output:
            self.fail("SECURITY VULNERABILITY: Error message leaks internal exception details")

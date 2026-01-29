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

if __name__ == '__main__':
    unittest.main()

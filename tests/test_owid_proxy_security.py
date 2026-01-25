import unittest
import unittest.mock
import sys
import os
import importlib.util
from io import BytesIO

# Load the module dynamically
file_path = os.path.join(os.path.dirname(__file__), "../web/5d-map/owid_proxy.py")
spec = importlib.util.spec_from_file_location("owid_proxy", file_path)
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)


class MockStreamResponse:
    def __init__(self, data, headers=None):
        self.data = data
        self.position = 0
        self.headers = headers or {}

    def read(self, size=None):
        if size is None:
            ret = self.data[self.position:]
            self.position = len(self.data)
            return ret
        else:
            ret = self.data[self.position:self.position + size]
            self.position += len(ret)
            return ret

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


# Helper class to override setup for testing
class TestHandler(owid_proxy.ProxyHandler):
    def __init__(self, request, client_address, server, rfile, wfile):
        self._rfile = rfile
        self._wfile = wfile
        super().__init__(request, client_address, server)

    def setup(self):
        self.rfile = self._rfile
        self.wfile = self._wfile
        # BaseHTTPRequestHandler.setup also sets self.connection = self.request
        self.connection = self.request

class TestOwidProxySecurity(unittest.TestCase):
    def setUp(self):
        self.handler_class = TestHandler
        # We need to mock the request and client_address for BaseHTTPRequestHandler
        self.mock_request = unittest.mock.Mock()
        self.mock_client_address = ('127.0.0.1', 12345)
        self.mock_server = unittest.mock.Mock()

    def test_security_headers(self):
        # Capture the output
        wfile = BytesIO()
        wfile.close = lambda: None # Prevent closing so we can read value
        rfile = BytesIO(b"GET /proxy/depression-prevalence.csv HTTP/1.1\r\nHost: localhost\r\n\r\n")

        # Mock urllib
        with unittest.mock.patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value = MockStreamResponse(b"some,csv,data")

            # Instantiate handler
            self.handler_class(self.mock_request, self.mock_client_address, self.mock_server, rfile, wfile)

            # To inspect headers, we look at wfile content.
            response = wfile.getvalue()

            # Should have response (even if headers are missing, at least 200 OK)
            self.assertIn(b"200 OK", response)

            # Check for X-Content-Type-Options: nosniff (Should fail currently)
            self.assertIn(b"X-Content-Type-Options: nosniff", response)

    def test_max_response_size_limit(self):
        # Capture the output
        wfile = BytesIO()
        wfile.close = lambda: None # Prevent closing so we can read value
        rfile = BytesIO(b"GET /proxy/depression-prevalence.csv HTTP/1.1\r\nHost: localhost\r\n\r\n")

        # Create a large payload > 10MB
        large_data = b"x" * (10 * 1024 * 1024 + 100) # 10MB + 100 bytes

        with unittest.mock.patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value = MockStreamResponse(large_data)

            # Instantiate handler
            self.handler_class(self.mock_request, self.mock_client_address, self.mock_server, rfile, wfile)

            response = wfile.getvalue()

            # It should fail with an error message or 502
            # Currently it likely returns 200 OK because the bug exists (no size limit)
            # So we assert that it DOES NOT contain 200 OK to verify the fix later?
            # Or we assert that it contains 502.
            # Since we are testing for the VULNERABILITY (or rather, the fix), let's assert what we WANT.
            # If it fails now, it means the code is not secure (good).

            self.assertIn(b"502 Bad Gateway", response)

if __name__ == '__main__':
    unittest.main()

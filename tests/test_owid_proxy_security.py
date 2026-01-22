import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import importlib.util
from io import BytesIO

# Load the owid_proxy module dynamically
PROXY_PATH = os.path.join(os.path.dirname(__file__), "../web/5d-map/owid_proxy.py")
spec = importlib.util.spec_from_file_location("owid_proxy", PROXY_PATH)
owid_proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owid_proxy)

class TestOwidProxySecurity(unittest.TestCase):
    def setUp(self):
        self.mock_request = MagicMock()
        self.mock_client_address = ('127.0.0.1', 12345)
        self.mock_server = MagicMock()

    def create_handler(self, path):
        # We mock the socket makefile to return a request line
        self.mock_request.makefile.return_value = BytesIO(f"GET /{path} HTTP/1.1\r\n\r\n".encode())

        handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        handler.request = self.mock_request
        handler.client_address = self.mock_client_address
        handler.server = self.mock_server
        handler.path = path
        handler.command = 'GET'
        handler.wfile = BytesIO()
        handler.headers = {}

        # BaseHTTPRequestHandler requires these for logging usually
        handler.requestline = f"GET /{path} HTTP/1.1"
        handler.request_version = "HTTP/1.1"

        return handler

    @patch('urllib.request.urlopen')
    def test_do_get_normal(self, mock_urlopen):
        """Verify normal operation."""
        mock_response = MagicMock()
        # side_effect allows us to return data then empty string (EOF)
        mock_response.read.side_effect = [b"csv,data\n1,2", b""]
        mock_response.getheader.return_value = "15"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        handler = self.create_handler("proxy/depression-prevalence.csv")
        handler.do_GET()

        output = handler.wfile.getvalue()
        self.assertIn(b"HTTP/1.0 200 OK", output)
        self.assertIn(b"csv,data", output)
        self.assertIn(b"X-Content-Type-Options: nosniff", output)

    @patch('urllib.request.urlopen')
    def test_do_get_too_large(self, mock_urlopen):
        """Verify DoS protection (size limit)."""
        mock_response = MagicMock()

        # Scenario 1: Content-Length header is too big
        mock_response.getheader.return_value = str(owid_proxy.MAX_RESPONSE_SIZE + 1)
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        handler = self.create_handler("proxy/depression-prevalence.csv")
        handler.do_GET()
        output = handler.wfile.getvalue()
        self.assertIn(b"Response too large", output)

        # Scenario 2: Content-Length okay (or missing), but body is too big
        mock_response.getheader.return_value = None
        # We simulate reading chunks.
        # Chunk 1: valid size.
        # Chunk 2: makes it overflow.
        chunk_size = owid_proxy.MAX_RESPONSE_SIZE // 2 + 1024
        mock_response.read.side_effect = [b"x" * chunk_size, b"x" * chunk_size, b""]

        handler = self.create_handler("proxy/depression-prevalence.csv")
        handler.do_GET()
        output = handler.wfile.getvalue()
        self.assertIn(b"Response too large", output)

    def test_invalid_path(self):
        handler = self.create_handler("proxy/invalid")
        handler.do_GET()
        output = handler.wfile.getvalue()
        self.assertIn(b"404 Not Found", output)
        self.assertIn(b"X-Content-Type-Options: nosniff", output)

if __name__ == '__main__':
    unittest.main()

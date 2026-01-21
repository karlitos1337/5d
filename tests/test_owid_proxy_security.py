import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import importlib.util
import io

# Load the module dynamically
file_path = os.path.join(os.path.dirname(__file__), '..', 'web', '5d-map', 'owid_proxy.py')
spec = importlib.util.spec_from_file_location("owid_proxy", file_path)
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)

class TestProxySecurity(unittest.TestCase):
    def setUp(self):
        self.handler_cls = owid_proxy.ProxyHandler
        self.mock_request = MagicMock()
        self.mock_client_address = ('127.0.0.1', 12345)
        self.mock_server = MagicMock()

    def create_handler(self):
        # Instantiate without calling __init__
        handler = self.handler_cls.__new__(self.handler_cls)
        handler.request = self.mock_request
        handler.client_address = self.mock_client_address
        handler.server = self.mock_server

        # BaseHTTPRequestHandler attributes
        handler.rfile = io.BytesIO()
        handler.wfile = io.BytesIO()
        handler.path = "/proxy/depression-prevalence.csv"
        handler.command = "GET"
        handler.headers = {}
        handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.0"

        handler.request_version = "HTTP/1.0"
        handler.protocol_version = "HTTP/1.0"
        handler.close_connection = True

        return handler

    @patch('urllib.request.urlopen')
    def test_security_headers_presence(self, mock_urlopen):
        """Test that X-Content-Type-Options: nosniff header is present."""
        # Setup mock response
        mock_resp = MagicMock()
        mock_resp.headers = {'Content-Length': '10'}
        # side_effect to simulate stream end: returns data then empty bytes
        mock_resp.read.side_effect = [b'testdata', b'']
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        handler = self.create_handler()

        # Execute
        handler.do_GET()

        # Verify
        output = handler.wfile.getvalue()
        self.assertIn(b"X-Content-Type-Options: nosniff", output, "Missing security header X-Content-Type-Options")

    @patch('urllib.request.urlopen')
    def test_max_response_size_content_length(self, mock_urlopen):
        """Test that requests with Content-Length > MAX_RESPONSE_SIZE are rejected."""
        mock_resp = MagicMock()
        # Set a huge content length (e.g., 20MB)
        mock_resp.getheader.side_effect = lambda k, d=None: "20971520" if k == "Content-Length" else d
        mock_resp.headers = {'Content-Length': '20971520'} # 20MB
        mock_resp.read.return_value = b''
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        handler = self.create_handler()
        handler.do_GET()

        output = handler.wfile.getvalue()
        # Checking for error response
        self.assertTrue(b"502" in output or b"413" in output, "Should reject large Content-Length")
        self.assertIn(b"too large", output.lower(), "Should mention size limit in error")

    @patch('urllib.request.urlopen')
    def test_max_response_size_during_read(self, mock_urlopen):
        """Test that reading stops if data exceeds limit (even if Content-Length is small or missing)."""
        mock_resp = MagicMock()
        mock_resp.headers = {} # No Content-Length

        # Simulate a stream that keeps giving data
        # 10MB limit. Let's give 10 chunks of 1.1MB
        chunk = b'x' * (1024 * 1024 + 100) # 1MB + 100 bytes
        # We need enough chunks to exceed 10MB. 10 chunks = 10MB + 1000 bytes > 10MB.
        mock_resp.read.side_effect = [chunk] * 10 + [b'']

        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        handler = self.create_handler()
        handler.do_GET()

        output = handler.wfile.getvalue()
        self.assertTrue(b"502" in output or b"413" in output, "Should reject when read exceeds limit")
        self.assertIn(b"too large", output.lower(), "Should mention size limit")

if __name__ == '__main__':
    unittest.main()

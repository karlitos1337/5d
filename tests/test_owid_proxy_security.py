import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO

# Add the web/5d-map directory to sys.path so we can import owid_proxy
sys.path.append(os.path.join(os.path.dirname(__file__), '../web/5d-map'))

import owid_proxy

class MockStreamResponse:
    def __init__(self, content, headers=None):
        self.content = content
        self.position = 0
        self.headers = headers or {}

    def read(self, size=-1):
        if size == -1:
            data = self.content[self.position:]
            self.position = len(self.content)
            return data

        if self.position >= len(self.content):
            return b""

        chunk = self.content[self.position:self.position + size]
        self.position += len(chunk)
        return chunk

    def getheader(self, name, default=None):
        return self.headers.get(name, default)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        self.request = MagicMock()
        self.client_address = ('127.0.0.1', 12345)
        self.server = MagicMock()

        self.wfile = BytesIO()
        self.wfile.close = lambda: None

    def _create_handler(self):
        handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        handler.client_address = self.client_address
        handler.server = self.server
        handler.path = "/proxy/depression-prevalence.csv"
        handler.command = "GET"
        handler.request_version = "HTTP/1.0"
        handler.headers = {}
        handler.rfile = BytesIO()
        handler.wfile = self.wfile
        handler.log_message = MagicMock()
        handler.log_error = MagicMock() # Mock log_error to verify it's called
        handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.0"
        return handler

    @patch('urllib.request.urlopen')
    def test_do_GET_security_headers(self, mock_urlopen):
        """Test that X-Content-Type-Options: nosniff header is present."""
        content = b"data"
        mock_urlopen.return_value = MockStreamResponse(content)

        handler = self._create_handler()
        handler.do_GET()

        response = self.wfile.getvalue().decode('utf-8', errors='ignore')
        self.assertIn("X-Content-Type-Options: nosniff", response)

    @patch('urllib.request.urlopen')
    def test_do_GET_too_large_streaming(self, mock_urlopen):
        """Test that requests exceeding MAX_RESPONSE_SIZE are truncated during streaming."""
        # 10MB + 8KB (one chunk size)
        limit = 10 * 1024 * 1024
        large_content = b"a" * (limit + 8192)
        mock_urlopen.return_value = MockStreamResponse(large_content)

        handler = self._create_handler()
        handler.do_GET()

        response_data = self.wfile.getvalue()

        # Extract body (skip headers)
        header_end = response_data.find(b"\r\n\r\n")
        body = response_data[header_end+4:]

        # Verify body size is <= limit
        self.assertLessEqual(len(body), limit)

        # Verify that we logged an error
        handler.log_error.assert_called_with("Response exceeded MAX_RESPONSE_SIZE (%d bytes)", limit)

    @patch('urllib.request.urlopen')
    def test_do_GET_too_large_content_length(self, mock_urlopen):
        """Test that requests with Content-Length > MAX_RESPONSE_SIZE are rejected immediately."""
        limit = 10 * 1024 * 1024
        headers = {"Content-Length": str(limit + 1)}
        mock_urlopen.return_value = MockStreamResponse(b"", headers=headers)

        handler = self._create_handler()
        handler.do_GET()

        response = self.wfile.getvalue().decode('utf-8', errors='ignore')

        # Should be 502 Bad Gateway
        self.assertIn("502 Bad Gateway", response)
        self.assertIn("Upstream request failed", response)

    @patch('urllib.request.urlopen')
    def test_do_GET_upstream_error_no_leak(self, mock_urlopen):
        """Test that upstream errors do not leak sensitive exception details."""
        secret = "SecretDBConnectionFailed"
        mock_urlopen.side_effect = Exception(secret)

        handler = self._create_handler()
        handler.do_GET()

        response = self.wfile.getvalue().decode('utf-8', errors='ignore')

        self.assertIn("502 Bad Gateway", response)
        self.assertNotIn(secret, response, "Exception message leaked in response body")
        self.assertIn("Upstream request failed", response)

if __name__ == "__main__":
    unittest.main()

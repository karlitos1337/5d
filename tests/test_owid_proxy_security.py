import unittest
from unittest.mock import MagicMock, patch
import importlib.util
import os
import io

# Import owid_proxy dynamically due to hyphen in path
spec = importlib.util.spec_from_file_location(
    "owid_proxy",
    os.path.join(os.path.dirname(__file__), "../web/5d-map/owid_proxy.py")
)
owid_proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owid_proxy)

class TestOwidProxySecurity(unittest.TestCase):
    def setUp(self):
        # Create handler bypassing __init__ to avoid socket binding
        self.handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        self.handler.wfile = io.BytesIO()
        self.handler.headers = {}
        self.handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"
        self.handler.request_version = "HTTP/1.1"
        self.handler.client_address = ("127.0.0.1", 12345)

    def test_response_size_limit_exceeded(self):
        """Test that the proxy rejects responses larger than 10MB."""
        self.handler.path = "/proxy/depression-prevalence.csv"

        # Mock urllib.request.urlopen
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()

            # Simulate a stream that never ends or is too large
            # We'll make it return 11MB of data in chunks
            chunk_size = 1024 * 1024 # 1MB
            chunks = [b"x" * chunk_size] * 11

            # Configure read side_effect to return chunks then empty bytes
            mock_response.__enter__.return_value = mock_response
            mock_response.read.side_effect = chunks + [b""]

            mock_urlopen.return_value = mock_response

            # Run do_GET
            self.handler.do_GET()

            # Get output
            output = self.handler.wfile.getvalue()

            # Verify it failed securely
            self.assertIn(b"Fetch error", output)
            self.assertIn(b"Response too large", output)

            # Verify 502 status (from exception handler)
            # send_response(502) writes "HTTP/1.0 502 Bad Gateway..." to wfile
            self.assertIn(b"502", output)

    def test_response_size_within_limit(self):
        """Test that the proxy accepts responses within the 10MB limit."""
        self.handler.path = "/proxy/depression-prevalence.csv"

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()

            # 1KB data
            data = b"x" * 1024

            mock_response.__enter__.return_value = mock_response
            # First read returns data, second returns empty (EOF)
            mock_response.read.side_effect = [data, b""]

            mock_urlopen.return_value = mock_response

            self.handler.do_GET()

            output = self.handler.wfile.getvalue()

            # Verify success
            self.assertIn(b"200 OK", output)
            # Body should contain the data
            self.assertTrue(output.endswith(data))

if __name__ == "__main__":
    unittest.main()

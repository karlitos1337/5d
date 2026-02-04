import importlib.util
import unittest
from unittest.mock import MagicMock, patch

# Load the module dynamically
spec = importlib.util.spec_from_file_location("owid_proxy", "web/5d-map/owid_proxy.py")
owid_proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owid_proxy)

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        # Create a dummy handler instance without calling __init__
        self.handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        self.handler.path = "/proxy/depression-prevalence.csv"
        self.handler.client_address = ('127.0.0.1', 12345)
        self.handler.request = MagicMock()
        self.handler.server = MagicMock()
        self.handler.command = "GET"
        self.handler.wfile = MagicMock()
        self.handler.headers = {}
        self.handler.request_version = "HTTP/1.1"
        self.handler.protocol_version = "HTTP/1.1"
        self.handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"

        # Mock methods
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock(side_effect=lambda k, v: self.handler.headers.update({k: v}))
        self.handler.end_headers = MagicMock()
        self.handler.log_message = MagicMock()

    @patch('urllib.request.urlopen')
    def test_dos_protection_max_size(self, mock_urlopen):
        """Test that the proxy rejects responses larger than the limit."""
        # 10MB + 1 byte
        large_size = 10 * 1024 * 1024 + 1

        mock_response = MagicMock()
        # Mock read to return small chunks that eventually sum up to large_size
        # But for simplicity, let's make the first chunk already too big, or use side_effect
        # If we change code to use chunked read, we need to handle that.

        # For the test, we want to ensure it handles "infinite" streams or just big files.
        # Let's mock a read() that returns a large blob.
        mock_response.read.return_value = b'x' * large_size

        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.handler.do_GET()

        # Expect failure (502 or custom error)
        # Check that we didn't write the full large data
        if self.handler.wfile.write.called:
            args, _ = self.handler.wfile.write.call_args
            self.assertLess(len(args[0]), large_size, "Should not write full large response back to client")

            # Should have error message (generic error to avoid leaking details, or specific safe error)
            # The implementation returns generic "Fetch error" for all exceptions
            self.assertIn(b"Fetch error", args[0])

    @patch('urllib.request.urlopen')
    def test_error_sanitization(self, mock_urlopen):
        """Test that internal exception details are not leaked."""
        secret_info = "secret_db_password"
        mock_urlopen.side_effect = Exception(f"Connection failed: {secret_info}")

        self.handler.do_GET()

        args, _ = self.handler.wfile.write.call_args
        response_body = args[0]

        self.assertNotIn(secret_info.encode(), response_body)
        self.assertIn(b"Fetch error", response_body)

    @patch('urllib.request.urlopen')
    def test_security_headers(self, mock_urlopen):
        """Test that security headers are added."""
        mock_response = MagicMock()
        # Return data then EOF
        mock_response.read.side_effect = [b"ok", b""]
        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.handler.do_GET()

        self.assertIn('X-Content-Type-Options', self.handler.headers)
        self.assertEqual(self.handler.headers['X-Content-Type-Options'], 'nosniff')

if __name__ == '__main__':
    unittest.main()

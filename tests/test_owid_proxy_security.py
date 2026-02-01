import unittest
from unittest.mock import MagicMock, patch, Mock
import sys
import os
import importlib.util

# Load the module dynamically
file_path = os.path.join(os.getcwd(), 'web/5d-map/owid_proxy.py')
spec = importlib.util.spec_from_file_location("owid_proxy", file_path)
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)

from owid_proxy import ProxyHandler

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        self.request_mock = Mock()
        self.wfile_mock = Mock()
        self.request_mock.wfile = self.wfile_mock
        self.client_address = ('127.0.0.1', 12345)
        self.server = Mock()

        # Instantiate without calling __init__
        self.handler = ProxyHandler.__new__(ProxyHandler)
        self.handler.client_address = self.client_address
        self.handler.request = self.request_mock
        self.handler.server = self.server
        self.handler.wfile = self.wfile_mock
        self.handler.command = 'GET'
        self.handler.path = "/proxy/depression-prevalence.csv"
        self.handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"

        # Mock header methods to avoid BaseHTTPRequestHandler logic
        self.headers = {}
        self.handler.send_response = Mock()
        def mock_send_header(k, v):
            self.headers[k] = v
        self.handler.send_header = Mock(side_effect=mock_send_header)
        self.handler.end_headers = Mock()

        # Suppress logging
        self.handler.log_request = Mock()
        self.handler.log_error = Mock()
        self.handler.log_message = Mock()

    def test_dos_protection_large_file(self):
        """Test that the proxy rejects files larger than MAX_RESPONSE_SIZE."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            # 11MB + 1 byte
            chunk_size = 1024 * 1024 # 1MB chunks
            chunks = [b'a' * chunk_size] * 11
            chunks.append(b'')
            mock_response.read.side_effect = chunks

            mock_urlopen.return_value.__enter__.return_value = mock_response

            self.handler.do_GET()

            # Verify that we got a 502 (or 500, but 502 is "Bad Gateway" often used for upstream issues)
            # OR just check the error message.
            # In my plan I said "Response too large".

            write_calls = self.wfile_mock.write.call_args_list
            output = b"".join([call[0][0] for call in write_calls])

            self.assertIn(b"Response too large", output)

    def test_error_sanitization(self):
        """Test that exception details are not leaked."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            # Simulate an error with a secret
            mock_urlopen.side_effect = Exception("Database password is distinct_secret_123")

            self.handler.do_GET()

            write_calls = self.wfile_mock.write.call_args_list
            output = b"".join([call[0][0] for call in write_calls])

            # Should NOT contain the secret
            self.assertNotIn(b"distinct_secret_123", output)
            # Should contain generic error
            self.assertIn(b"Fetch error", output)

    def test_security_headers(self):
        """Test that security headers are present."""
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = b"csv,data"
            mock_urlopen.return_value.__enter__.return_value = mock_response

            # Since read() returns bytes directly (not chunks via side_effect in this simple case),
            # the current implementation works fine.
            # The mocked read needs to handle being called multiple times if the new implementation loops.
            # side_effect=[b"csv,data", b""] handles loop.
            mock_response.read.side_effect = [b"csv,data", b""]

            self.handler.do_GET()

            self.assertIn("X-Content-Type-Options", self.headers)
            self.assertEqual(self.headers["X-Content-Type-Options"], "nosniff")

if __name__ == '__main__':
    unittest.main()

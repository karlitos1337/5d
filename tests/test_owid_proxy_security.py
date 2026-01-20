import importlib.util
import os
import unittest
from unittest.mock import MagicMock, patch

# Import owid_proxy.py dynamically
PROXY_PATH = os.path.join(os.getcwd(), 'web/5d-map/owid_proxy.py')
spec = importlib.util.spec_from_file_location("owid_proxy", PROXY_PATH)
owid_proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owid_proxy)

class TestOWIDProxySecurity(unittest.TestCase):

    def setUp(self):
        self.request = MagicMock()
        self.client_address = ('127.0.0.1', 12345)
        self.server = MagicMock()

        # Instantiate handler but don't call __init__ to avoid socket setup
        # We will manually set up what we need
        self.handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        self.handler.request = self.request
        self.handler.client_address = self.client_address
        self.handler.server = self.server
        self.handler.wfile = MagicMock()
        self.handler.rfile = MagicMock()

        # Mock send_header to inspect headers
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.send_response = MagicMock()

        # BaseHTTPRequestHandler attributes needed for logging/responses
        self.handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"
        self.handler.request_version = "HTTP/1.1"
        self.handler.client_address = self.client_address
        self.handler.path = "/proxy/depression-prevalence.csv"

    @patch('urllib.request.urlopen')
    def test_response_size_limit(self, mock_urlopen):
        """Test that the proxy enforces a response size limit (DoS protection)."""
        # Mock a response that yields infinite data or just too much data
        mock_response = MagicMock()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # 11MB of data
        large_data = b'x' * (10 * 1024 * 1024 + 1024)

        # If the code uses read(), it gets everything.
        # If it uses read(chunk), we simulate chunked behavior.
        # But here we want to verifying failure of the CURRENT code (which does read())
        # and success of NEW code (which should stop early).

        # For the mock, we can just make read() return the large data
        mock_response.read.side_effect = [large_data]

        # We need to spy on how read is called or catch the error we intend to raise
        # For now, let's assume the current code will just process it (success)
        # And the new code should raise an error or write an error response.

        self.handler.do_GET()

        # Verify headers - checking for security enhancement
        # Using a list of (key, value) tuples from call_args_list of send_header
        headers = {}
        for call in self.handler.send_header.call_args_list:
            headers[call[0][0]] = call[0][1]

        # This assertion is expected to FAIL until we add the fix
        self.assertIn('X-Content-Type-Options', headers, "Missing X-Content-Type-Options header")
        self.assertEqual(headers.get('X-Content-Type-Options'), 'nosniff')

        # Check for error response if limit exceeded (future behavior)
        # Current behavior writes 200 OK with large data.
        # We want to assert that we DO NOT write 11MB of data to wfile in the fixed version.

        # If the fix works, it should probably return a 502 or 500, or just stop writing.
        # Let's check if the write was called with the full large_data.

        written_data = b"".join(call[0][0] for call in self.handler.wfile.write.call_args_list)

        # The test expects protection: so verify we did NOT write the full amount
        # This will fail on current code because it writes everything
        self.assertLess(len(written_data), 10 * 1024 * 1024 + 100, "Response too large, DoS protection failed")

    @patch('urllib.request.urlopen')
    def test_chunked_read_implementation(self, mock_urlopen):
        """Verify that we are actually reading in chunks, not all at once."""
        mock_response = MagicMock()
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_response.read.return_value = b'small'

        self.handler.do_GET()

        # If the code calls read() (no args), it reads everything.
        # If it calls read(8192) or similar, it's chunked.
        # We want to enforce chunked reading.

        # This assertion will FAIL on current code
        # We check that read was called with an argument (chunk size)
        # mock_response.read.assert_called_with() would pass for current code

        # We want to verify it was called WITH arguments (e.g., read(8192))
        # OR called multiple times.

        # Actually, simpler: Assert that we don't call read() without arguments.
        # But read() without arguments is valid for small files?
        # No, for DoS protection we NEVER want to call read() without limit.

        calls = mock_response.read.call_args_list
        for call in calls:
            args, _ = call
            if not args:
                self.fail("Security Risk: read() called without size limit!")

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add web/5d-map directory to path to import owid_proxy
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(root_dir, 'web', '5d-map'))

import owid_proxy

class MockResponse:
    def __init__(self, content=b"", stream_content=None):
        self.content = content
        self.stream_content = stream_content or [content]
        self.headers = {"Content-Length": str(len(content))}

    def read(self, size=None):
        if size is None:
            # Read everything remaining
            res = b"".join(self.stream_content)
            self.stream_content = []
            return res

        if not self.stream_content:
            return b""

        chunk = self.stream_content[0]
        if len(chunk) > size:
            self.stream_content[0] = chunk[size:]
            return chunk[:size]
        else:
            self.stream_content.pop(0)
            return chunk

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        # Bypass __init__ to avoid socket interactions
        self.handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)

        # Manually set attributes needed by do_GET
        self.handler.path = ""
        self.handler.wfile = MagicMock()
        self.handler.rfile = MagicMock()
        self.handler.client_address = ('127.0.0.1', 12345)
        self.handler.server = MagicMock()

        # Mock methods called by do_GET
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()
        self.handler.log_message = MagicMock()

    @patch('urllib.request.urlopen')
    def test_proxy_normal_file(self, mock_urlopen):
        # Setup mock to return a small CSV
        csv_content = b"country,value\nUSA,10\n"
        mock_urlopen.return_value = MockResponse(content=csv_content)

        # Setup request path
        self.handler.path = "/proxy/depression-prevalence.csv"

        # Run do_GET
        self.handler.do_GET()

        # Verify response
        self.handler.send_response.assert_called_with(200)
        self.handler.wfile.write.assert_called()

        writes = [call.args[0] for call in self.handler.wfile.write.call_args_list]
        full_output = b"".join(writes)
        self.assertEqual(full_output, csv_content)

    @patch('urllib.request.urlopen')
    def test_proxy_large_file_prevention(self, mock_urlopen):
        limit = 10 * 1024 * 1024
        chunk_size = 1024 * 1024 # 1MB

        # 11 chunks of 1MB = 11MB
        chunks = [b"a" * chunk_size] * 11

        mock_urlopen.return_value = MockResponse(stream_content=list(chunks))

        self.handler.path = "/proxy/depression-prevalence.csv"

        self.handler.do_GET()

        # In the SECURE version, it should abort before reading everything

        # Check if 502 was sent
        self.handler.send_response.assert_called_with(502)

        writes = [call.args[0] for call in self.handler.wfile.write.call_args_list]
        output = b"".join(writes)

        # Check that we got an error message
        self.assertIn(b"Fetch error", output)
        self.assertIn(b"Response too large", output)

        # Check that we did NOT write the full 11MB content
        self.assertLess(len(output), 1000) # Error message is short

if __name__ == '__main__':
    unittest.main()

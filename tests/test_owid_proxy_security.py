import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import io

# Add the directory containing the proxy to the path
sys.path.append(os.path.abspath("web/5d-map"))

import owid_proxy

class TestOWIDProxySecurity(unittest.TestCase):
    def test_rejects_large_files(self):
        """Test that files larger than 10MB are rejected."""
        # Mocking BaseHTTPRequestHandler is tricky because it calls setup() in __init__
        # We will subclass it to override setup/init or use a helper

        # Instead, let's just instantiate ProxyHandler with mocks that satisfy BaseHTTPRequestHandler
        # BaseHTTPRequestHandler.__init__ calls:
        #   self.request = request
        #   self.client_address = client_address
        #   self.server = server
        #   self.setup()
        #   try: self.handle() finally: self.finish()

        # We can bypass __init__ and call do_GET directly if we setup the instance manually
        handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        handler.wfile = io.BytesIO()
        handler.rfile = io.BytesIO()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        handler.log_message = MagicMock()
        handler.path = "/proxy/depression-prevalence.csv"

        limit = 10 * 1024 * 1024
        large_content = b"a" * (limit + 1024) # 10MB + 1KB

        # Mock urllib.request.urlopen
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = large_content
            mock_response.info.return_value = {"Content-Length": str(len(large_content))}
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response

            # Execute
            handler.do_GET()

            # Verification
            # Check status code sent
            if handler.send_response.call_count > 0:
                args, _ = handler.send_response.call_args
                status_code = args[0]

                if status_code == 200:
                    print(f"VULNERABILITY CONFIRMED: Server accepted {len(large_content)} bytes")
                    self.fail("Server accepted a file larger than 10MB")
                else:
                    print(f"Server rejected large file with status {status_code} (Secure behavior)")
            else:
                 self.fail("send_response was not called")

if __name__ == "__main__":
    unittest.main()

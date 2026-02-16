import http.client
import os
import sys
import threading
import time
import unittest
from http.server import HTTPServer
from unittest.mock import MagicMock, patch

# Add the parent directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import owid_proxy


class TestOWIDProxy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Find a free port
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        cls.port = sock.getsockname()[1]
        sock.close()

        # Start the server in a separate thread
        cls.server = HTTPServer(('127.0.0.1', cls.port), owid_proxy.ProxyHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_headers_root(self):
        """Test headers on root path (404)."""
        # Use http.client to avoid potential interference if we were patching globally
        conn = http.client.HTTPConnection('127.0.0.1', self.port)
        conn.request("GET", "/")
        response = conn.getresponse()

        self.assertEqual(response.status, 404)
        self.assertEqual(response.getheader("X-Content-Type-Options"), "nosniff")
        conn.close()

    def test_headers_success(self):
        """Test headers on successful proxy request."""
        # We patch urllib.request.urlopen in the owid_proxy module
        mock_resp = MagicMock()
        mock_resp.read.return_value = b"test,data"
        mock_resp.__enter__.return_value = mock_resp

        # Patching inside the module where it is used. Since owid_proxy imports urllib.request,
        # we can try to patch 'owid_proxy.urllib.request.urlopen'.
        # However, since it is a system module, it patches it globally.
        # We use http.client for our request to avoid hitting the patch.

        with patch('urllib.request.urlopen', return_value=mock_resp):
            conn = http.client.HTTPConnection('127.0.0.1', self.port)
            conn.request("GET", "/proxy/depression-prevalence.csv")
            response = conn.getresponse()

            self.assertEqual(response.status, 200)
            self.assertEqual(response.getheader("X-Content-Type-Options"), "nosniff")
            self.assertEqual(response.getheader("Content-Security-Policy"), "default-src 'none'; frame-ancestors 'none'")
            self.assertEqual(response.getheader("X-Frame-Options"), "DENY")
            self.assertEqual(response.read(), b"test,data")
            conn.close()

if __name__ == "__main__":
    unittest.main()

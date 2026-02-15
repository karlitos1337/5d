import sys
import os
import threading
import time
import urllib.request
import unittest
from http.server import HTTPServer

# Add parent directory to path to import owid_proxy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import owid_proxy

class TestProxy(unittest.TestCase):
    def setUp(self):
        self.port = 5511
        # We manually bind to 127.0.0.1 here to test the handler logic
        self.server = HTTPServer(("127.0.0.1", self.port), owid_proxy.ProxyHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(1)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=1)

    def test_security_headers(self):
        url = f"http://127.0.0.1:{self.port}/proxy/depression-prevalence.csv"
        try:
            # We expect a 200 if internet is available, or 502 if not.
            # In sandbox, internet might be available.
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
                self.assertEqual(response.headers.get("Content-Security-Policy"), "default-src 'none'; frame-ancestors 'none'")
                self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
                self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
        except urllib.error.HTTPError as e:
            # Even on error, security headers should be present
            self.assertEqual(e.headers.get("X-Content-Type-Options"), "nosniff")
            self.assertEqual(e.headers.get("Access-Control-Allow-Origin"), "*")

if __name__ == "__main__":
    unittest.main()

import http.client
import os
import sys
import threading
import time
import unittest

# Add parent directory to path to import owid_proxy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the module to test
import owid_proxy


class TestProxy(unittest.TestCase):
    def setUp(self):
        self.server = None
        self.thread = None
        self.port = 5511 # Use a different port for testing to avoid conflicts

    def tearDown(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=2)

    def start_server(self):
        # We bind to 127.0.0.1 for the test explicitly to ensure we can connect,
        # but the test logic below will verify the *default* binding logic by inspecting the code or behavior?
        # Actually, unit testing the binding logic is hard without mocking sys.argv or main().
        # Here we test the Handler logic (headers, error sanitization).

        self.server = owid_proxy.HTTPServer(("127.0.0.1", self.port), owid_proxy.ProxyHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(0.5) # Give it a moment to start

    def test_security_headers_present(self):
        self.start_server()
        conn = http.client.HTTPConnection("127.0.0.1", self.port)

        # Request a non-existent key to trigger a simple response
        conn.request("GET", "/proxy/invalid_key")
        response = conn.getresponse()
        response.read() # Consume body

        # Check for security headers
        headers = {k.lower(): v for k, v in response.getheaders()}

        self.assertIn("x-content-type-options", headers, "X-Content-Type-Options header missing")
        self.assertEqual(headers["x-content-type-options"], "nosniff")

        self.assertIn("content-security-policy", headers, "Content-Security-Policy header missing")
        self.assertIn("default-src 'none'", headers["content-security-policy"])

        self.assertIn("x-frame-options", headers, "X-Frame-Options header missing")
        self.assertEqual(headers["x-frame-options"], "DENY")

        conn.close()

    def test_error_sanitization(self):
        # To test error sanitization, we need to trigger an exception in do_GET.
        # We can mock urllib.request.urlopen to raise an exception.

        original_urlopen = owid_proxy.urllib.request.urlopen

        def mock_urlopen(*args, **kwargs):
            raise Exception("Sensitive internal info")

        owid_proxy.urllib.request.urlopen = mock_urlopen

        try:
            self.start_server()
            conn = http.client.HTTPConnection("127.0.0.1", self.port)

            # Request a valid key but force an error
            # We need a valid key from OWID_URLS to enter the try block
            valid_key = list(owid_proxy.OWID_URLS.keys())[0]
            conn.request("GET", f"/proxy/{valid_key}")

            response = conn.getresponse()
            body = response.read().decode('utf-8')

            self.assertEqual(response.status, 502)
            self.assertNotIn("Sensitive internal info", body, "Error message leaked internal exception details")
            self.assertIn("Fetch error", body) # We can keep "Fetch error" but not the details

            conn.close()
        finally:
            owid_proxy.urllib.request.urlopen = original_urlopen

if __name__ == "__main__":
    unittest.main()

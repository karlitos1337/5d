import importlib.util
import sys
import threading
import time
import unittest
from http.server import HTTPServer
from unittest.mock import patch
from urllib.request import urlopen

# Load the module dynamically
spec = importlib.util.spec_from_file_location("owid_proxy", "web/5d-map/owid_proxy.py")
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)


class MockStreamResponse:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def read(self, size=-1):
        if size == -1:
            ret = self.data[self.pos :]
            self.pos = len(self.data)
            return ret
        if self.pos >= len(self.data):
            return b""
        ret = self.data[self.pos : self.pos + size]
        self.pos += size
        return ret

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class TestOWIDProxySecurityReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 5515
        cls.server = HTTPServer(("localhost", cls.port), owid_proxy.ProxyHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_security_headers(self):
        """Verify that security headers are present."""
        mock_response = MockStreamResponse(b"test,data")

        with patch("owid_proxy.urllib.request.urlopen", return_value=mock_response):
            url = f"http://localhost:{self.port}/proxy/depression-prevalence.csv"
            with urlopen(url) as response:
                headers = response.headers
                self.assertIn("X-Content-Type-Options", headers)
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
                self.assertIn("Access-Control-Allow-Origin", headers)
                self.assertEqual(response.read(), b"test,data")

    def test_large_response_dos_protection(self):
        """Verify that responses larger than limit are rejected."""
        # 11MB chunk
        large_chunk = b"x" * (11 * 1024 * 1024)
        mock_response = MockStreamResponse(large_chunk)

        with patch("owid_proxy.urllib.request.urlopen", return_value=mock_response):
            url = f"http://localhost:{self.port}/proxy/depression-prevalence.csv"
            try:
                with urlopen(url):
                    pass
            except Exception as e:
                # urlopen raises HTTPError for 5xx
                # We expect 502
                self.assertIn("HTTP Error 502", str(e))
                # How to verify the body message "Response too large" with urlopen exception?
                # e.read() might work if available, or we check e.code
                if hasattr(e, "code"):
                    self.assertEqual(e.code, 502)
                return

            self.fail("Server did not reject large response")


if __name__ == "__main__":
    unittest.main()

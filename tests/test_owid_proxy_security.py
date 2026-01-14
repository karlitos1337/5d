import unittest
from unittest.mock import MagicMock, patch, PropertyMock
import sys
import os
import importlib.util
from io import BytesIO

# Import helper for module with hyphen
def import_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load the module
owid_proxy = import_module_from_path("owid_proxy", "web/5d-map/owid_proxy.py")

class MockResponse:
    def __init__(self, data):
        self.data = data
        self.read_count = 0

    def read(self, size=None):
        if size is None:
            return self.data
        # Simple chunking simulation if needed, but for now just return all
        return self.data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class InfiniteResponse:
    def __init__(self):
        self.chunk = b"A" * 1024 * 1024 # 1MB chunk
        self.read_calls = 0

    def read(self, size=None):
        # Always return data to simulate infinite stream
        self.read_calls += 1
        if self.read_calls > 15: # Stop eventually to prevent test hang if logic is wrong
            return b""
        return self.chunk

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class TestOWIDProxySecurity(unittest.TestCase):
    def setUp(self):
        pass

    def create_handler(self, path):
        request = MagicMock()
        # Mock wfile as BytesIO so we can check what was written
        self.wfile = BytesIO()
        request.makefile.return_value = BytesIO() # rfile

        # We need to bypass BaseHTTPRequestHandler.__init__ or mock its dependencies perfectly
        # easier to just patch the class methods I don't need or instantiate carefully.
        # But BaseHTTPRequestHandler calls setup() and handle() in init.

        # Let's just create the instance and patch wfile AFTER? No, init uses it.
        # Let's mock the socket (request)

        server = MagicMock()

        # We can also just subclass ProxyHandler and override __init__
        class TestableHandler(owid_proxy.ProxyHandler):
            def __init__(self, path, wfile):
                self.path = path
                self.wfile = wfile
                self.headers = {}

            def send_response(self, code, message=None):
                self.code = code

            def send_header(self, keyword, value):
                self.headers[keyword] = value

            def end_headers(self):
                pass

        return TestableHandler(path, self.wfile)

    @patch('urllib.request.urlopen')
    def test_do_GET_valid_small_file(self, mock_urlopen):
        # Setup mock response
        mock_content = b"header1,header2\nval1,val2"
        mock_resp = MagicMock()
        mock_resp.__enter__.return_value = mock_resp
        # read() side effect: return content first call, empty bytes second call
        mock_resp.read.side_effect = [mock_content, b""]
        mock_urlopen.return_value = mock_resp

        handler = self.create_handler("/proxy/depression-prevalence.csv")
        handler.do_GET()

        # Verify success
        self.assertEqual(handler.code, 200)
        self.assertEqual(handler.wfile.getvalue(), mock_content)

    @patch('urllib.request.urlopen')
    def test_do_GET_dos_prevention(self, mock_urlopen):
        # Setup infinite/large response
        # We want to verify that it raises an error or stops reading when it hits the limit

        # We'll use a side_effect for read to return chunks
        # Total 11 chunks of 1MB = 11MB > 10MB limit
        chunk = b"X" * (1024 * 1024)
        chunks = [chunk] * 11 + [b""]

        mock_resp = MagicMock()
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.read.side_effect = chunks
        mock_urlopen.return_value = mock_resp

        handler = self.create_handler("/proxy/depression-prevalence.csv")

        # This should currently FAIL (it will read all chunks effectively if the code did loop,
        # but the current code calls read() with no args).
        # Wait, the current code calls `data = resp.read()`.
        # If I mock `read()` with no args to return 11MB, it will return 11MB.
        # I want to test that the NEW code handles it.
        # But to verify the FIX, I need the test to mimic the scenario.

        # Scenario: Upstream sends huge data.
        # If I mock read() to return a huge string:
        huge_data = b"X" * (15 * 1024 * 1024) # 15MB
        mock_resp.read.side_effect = None
        mock_resp.read.return_value = huge_data

        handler.do_GET()

        # With current code: It reads 15MB, sends 200 OK.
        # With fix: It should detect size > 10MB and fail (502 or similar).

        # Verification: Check that we eventually get an error response OR the data written is not the full 15MB.
        # But wait, if I mock read() to return 15MB at once, the `resp.read()` call consumes it all.
        # The FIX will involve changing `resp.read()` to `resp.read(CHUNK_SIZE)`.

        # So I need my mock to support `read(size)`.

        def layered_read(size=None):
            if size is None:
                return huge_data
            if size > len(huge_data):
                return huge_data
            return huge_data[:size] # This is a bit simplistic, doesn't maintain state

        # Better mock with state
        class StatefulMockResponse:
            def __init__(self, data):
                self.data = data
                self.pos = 0

            def read(self, size=None):
                if size is None:
                    ret = self.data[self.pos:]
                    self.pos = len(self.data)
                    return ret

                ret = self.data[self.pos:self.pos+size]
                self.pos += size
                return ret

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        mock_urlopen.return_value = StatefulMockResponse(huge_data)

        handler.do_GET()

        # Expect failure (502 or custom error)
        # Note: In the fix I will probably catch the size error and send 502.
        self.assertNotEqual(handler.code, 200, "Should not return 200 for file > 10MB")
        # Ensure we didn't write the full 15MB
        self.assertLess(len(handler.wfile.getvalue()), 15 * 1024 * 1024)

if __name__ == '__main__':
    unittest.main()

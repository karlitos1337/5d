import os
import sys
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

# Add web/5d-map to path to import owid_proxy
sys.path.append(os.path.join(os.getcwd(), "web/5d-map"))

from owid_proxy import ProxyHandler


class TestProxySecurity(unittest.TestCase):
    def setUp(self):
        pass

    def _get_handler(self):
        # Helper to get a configured handler instance without running __init__
        handler = ProxyHandler.__new__(ProxyHandler)
        handler.request = MagicMock()
        handler.client_address = ("127.0.0.1", 8888)
        handler.server = MagicMock()
        handler.command = "GET"
        handler.path = "/proxy/depression-prevalence.csv"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = BytesIO()
        handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"
        handler.log_request = MagicMock()
        return handler

    def test_error_leakage(self):
        """Test that exception details are NOT leaked to the client."""
        handler = self._get_handler()

        secret_message = "SECRET_STACK_TRACE_DETAILS"
        with patch("urllib.request.urlopen", side_effect=Exception(secret_message)):
            handler.do_GET()

        output = handler.wfile.getvalue()

        # Verify that we got a 502
        self.assertIn(b"502 Bad Gateway", output)
        # Verify strict no-leakage
        self.assertNotIn(secret_message.encode(), output)
        self.assertIn(b"Fetch error", output)  # Generic message
        # Verify security header
        self.assertIn(b"X-Content-Type-Options: nosniff", output)

    def test_large_response_dos(self):
        """Test that the proxy rejects responses larger than 10MB."""
        handler = self._get_handler()

        # Simulate 11MB response
        # We need to mock read(chunk_size) to return chunks
        total_size = 11 * 1024 * 1024

        # Generator for chunks
        def chunk_generator(size=None):
            bytes_yielded = 0
            while bytes_yielded < total_size:
                # If size is specified (read(N)), yield N bytes.
                # If size is None (read()), yield everything (old behavior simulation)
                # But the FIX will call read(8192)
                yield_size = size if size else (total_size - bytes_yielded)
                yield b"x" * yield_size
                bytes_yielded += yield_size

        # Since checking calls is complex, let's just make read return a chunk
        # But we need to maintain state.

        mock_resp = MagicMock()

        # State for side_effect
        state = {"yielded": 0}

        def read_side_effect(size=-1):
            if size == -1 or size is None:
                # If code calls read() without args (old behavior), return everything
                remaining = total_size - state["yielded"]
                state["yielded"] = total_size
                return b"x" * remaining
            else:
                # Code calls read(chunk_size)
                remaining = total_size - state["yielded"]
                if remaining <= 0:
                    return b""
                to_yield = min(size, remaining)
                state["yielded"] += to_yield
                return b"x" * to_yield

        mock_resp.read.side_effect = read_side_effect
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.__exit__.return_value = None

        with patch("urllib.request.urlopen", return_value=mock_resp):
            handler.do_GET()

        output = handler.wfile.getvalue()

        # Should NOT return 200 OK
        # Or if it returned 200 OK initially, the body should be truncated or it should have errored out mid-stream?
        # Ideally, we check the length or if it sent an error.

        # If the code raises exception after 10MB, it might catch it and send 502.
        # But headers are already sent (200 OK) before streaming usually?
        # The current code sends headers *after* reading everything.
        # The NEW code:
        # If we buffer everything in memory check size:
        #   If > 10MB, send 502/413.
        #   If < 10MB, send 200 and data.
        # Wait, if I read in chunks to avoid memory issues, I still need to decide whether to send 200 or 502.
        # If I send 200 first, I can't change it to 502 later.
        # But if I buffer up to 10MB, I can decide.
        # So the plan implies buffering up to 10MB.

        # If the stream is > 10MB:
        # We read 10MB. We see there is more. We abort.
        # Since we haven't sent headers yet (assuming we buffer), we can send 502/413.

        self.assertNotIn(b"200 OK", output)
        self.assertIn(b"Response too large", output)  # Expect this error message


if __name__ == "__main__":
    unittest.main()

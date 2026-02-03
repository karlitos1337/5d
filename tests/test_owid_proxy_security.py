import importlib.util
import os
import sys
import unittest
from io import BytesIO
from unittest.mock import MagicMock, patch

# Dynamically import the module because "5d-map" has a hyphen
file_path = os.path.join(os.getcwd(), "web/5d-map/owid_proxy.py")
spec = importlib.util.spec_from_file_location("owid_proxy", file_path)
owid_proxy = importlib.util.module_from_spec(spec)
sys.modules["owid_proxy"] = owid_proxy
spec.loader.exec_module(owid_proxy)


class TestProxySecurity(unittest.TestCase):
    def test_error_leakage(self):
        # Setup
        mock_request = MagicMock()
        output_buffer = BytesIO()

        handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        handler.request = mock_request
        handler.client_address = ("127.0.0.1", 8888)
        handler.server = MagicMock()
        handler.wfile = output_buffer
        handler.path = "/proxy/depression-prevalence.csv"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.protocol_version = "HTTP/1.1"
        handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"
        handler.headers = {}
        handler.log_message = MagicMock()

        # Mock urllib to simulate a failure with sensitive info
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.side_effect = Exception("SENSITIVE_DB_PASSWORD_12345")

            # Run the method
            handler.do_GET()

            # Check output
            output = output_buffer.getvalue()

            # NOW we expect NO sensitive string
            self.assertNotIn(b"SENSITIVE_DB_PASSWORD_12345", output)
            self.assertIn(b"Fetch error", output)
            print("\n[VERIFIED] Error message sanitized (no leak).")

    def test_dos_protection(self):
        """Test that we stop reading if response is too large"""
        mock_request = MagicMock()
        output_buffer = BytesIO()

        handler = owid_proxy.ProxyHandler.__new__(owid_proxy.ProxyHandler)
        handler.request = mock_request
        handler.client_address = ("127.0.0.1", 8888)
        handler.server = MagicMock()
        handler.wfile = output_buffer
        handler.path = "/proxy/depression-prevalence.csv"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.protocol_version = "HTTP/1.1"
        handler.requestline = "GET /proxy/depression-prevalence.csv HTTP/1.1"
        handler.headers = {}
        handler.log_message = MagicMock()

        # Create a mock response that simulates a never-ending stream (or very large)
        # We'll make it return chunks that sum up to > 10MB

        chunk_size = 1024 * 1024  # 1 MB

        # We need to simulate multiple read() calls.
        # The loop calls resp.read(8192).
        # To make it faster, let's mock read() to return 1MB chunks (even if requested 8KB, mock can return whatever)
        # Wait, if code asks for 8192, and we return 1MB, it's fine python-wise.

        chunks = [b"A" * chunk_size] * 12  # 12 MB total
        chunks.append(b"")  # End of stream

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            # We use side_effect with an iterator
            mock_response.read.side_effect = chunks
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response

            # Run the method
            handler.do_GET()

            output = output_buffer.getvalue()

            # It should fail and write "Fetch error" (because ValueError "Response too large" is caught)
            self.assertIn(b"Fetch error", output)

            # Verify we didn't crash
            print("\n[VERIFIED] DoS protection active (large response blocked).")


if __name__ == "__main__":
    unittest.main()

import threading
import time
import urllib.request
import urllib.error
import sys
import os
from http.server import HTTPServer

# Add the parent directory to sys.path to import owid_proxy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import owid_proxy

SERVER_PORT = 5511
SERVER_HOST = "127.0.0.1"
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

def run_server():
    server = HTTPServer((SERVER_HOST, SERVER_PORT), owid_proxy.ProxyHandler)
    server.serve_forever()

def check_headers(url, expected_headers):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = response.info()
            for header, value in expected_headers.items():
                if header not in headers:
                    return False, f"Missing header: {header}"
                if value and value not in headers[header]:
                    return False, f"Header {header} mismatch: expected {value}, got {headers[header]}"
            return True, "OK"
    except urllib.error.HTTPError as e:
        headers = e.headers
        for header, value in expected_headers.items():
            if header not in headers:
                return False, f"Missing header: {header} in error response {e.code}"
            if value and value not in headers[header]:
                return False, f"Header {header} mismatch in error response: expected {value}, got {headers[header]}"
        return True, "OK"
    except Exception as e:
        return False, f"Request failed: {e}"

def test_proxy_security():
    print(f"🚀 Starting test server on {SERVER_URL}...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Give it time to start

    expected_security_headers = {
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'none'",
        "X-Frame-Options": "DENY"
    }

    # 1. Test 404 path
    print("\n🔍 Testing 404 path...")
    success, msg = check_headers(f"{SERVER_URL}/unknown", expected_security_headers)
    assert success, f"404 Security Headers Check Failed: {msg}"
    print("✅ Security headers present on 404 response")

    # 2. Test valid proxy path
    print("\n🔍 Testing proxy path...")
    success, msg = check_headers(f"{SERVER_URL}/proxy/depression-prevalence.csv", expected_security_headers)
    # We assert success only if it's a header failure. Connection failure (e.g. upstream timeout)
    # might happen in CI if network is restricted, but the proxy should still return headers on error?
    # Actually, my proxy only sends headers if it catches an exception and returns 502.
    # If connection fails completely locally, check_headers returns False.
    # But running locally with 127.0.0.1 should work.

    # Wait, check_headers catches exceptions. If upstream fails, proxy catches it and returns 502 with headers.
    # So check_headers receives 502 and checks headers. So it should pass even if upstream is down.
    assert success, f"Proxy Security Headers Check Failed: {msg}"

    print("\n✅ Test completed.")

if __name__ == "__main__":
    test_proxy_security()

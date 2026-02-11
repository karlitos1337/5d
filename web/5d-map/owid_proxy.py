#!/usr/bin/env python3
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}

# Simple in-memory cache: {key: (data, timestamp)}
CACHE = {}
CACHE_TTL = 3600  # 1 hour


class ProxyHandler(BaseHTTPRequestHandler):
    def _set_security_headers(self):
        """Adds security headers to response."""
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'")
        self.send_header("X-Frame-Options", "DENY")
        # CORS (still needed for frontend access)
        self.send_header("Access-Control-Allow-Origin", "*")

    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            try:
                key = path.split("/", 1)[1]
            except IndexError:
                key = ""

            url = OWID_URLS.get(key)
            if not url:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self._set_security_headers()
                self.end_headers()
                self.wfile.write(b"Unknown proxy key")
                return

            # Check Cache
            now = time.time()
            if key in CACHE:
                data, timestamp = CACHE[key]
                if now - timestamp < CACHE_TTL:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("X-Cache", "HIT")
                    self._set_security_headers()
                    self.end_headers()
                    self.wfile.write(data)
                    return

            try:
                # Sentinel: Added timeout=15 to prevent hanging
                with urllib.request.urlopen(url, timeout=15) as resp:
                    data = resp.read()
                    # Update Cache
                    CACHE[key] = (data, now)

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("X-Cache", "MISS")
                    self._set_security_headers()
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                msg = f"Fetch error: {e}".encode()
                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self._set_security_headers()
                self.end_headers()
                self.wfile.write(msg)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self._set_security_headers()
            self.end_headers()
            self.wfile.write(b"Use /proxy/<file>")

    def log_message(self, fmt, *args):
        # Quiet log
        pass


def main():
    port = 5510
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    # Sentinel: Bind to 127.0.0.1 (localhost) instead of 0.0.0.0 for security
    server = HTTPServer(("127.0.0.1", port), ProxyHandler)
    print(f"OWID proxy listening on http://127.0.0.1:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

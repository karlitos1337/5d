#!/usr/bin/env python3
import os
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}


class ProxyHandler(BaseHTTPRequestHandler):
    def _set_security_headers(self):
        """Add security headers to response."""
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.send_header("X-Frame-Options", "DENY")
        # CORS (still needed for frontend fetch)
        self.send_header("Access-Control-Allow-Origin", "*")

    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            key = path.split("/", 1)[1]
            url = OWID_URLS.get(key)
            if not url:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self._set_security_headers()
                self.end_headers()
                self.wfile.write(b"Unknown proxy key")
                return
            try:
                # Add User-Agent to avoid blocking
                req = urllib.request.Request(
                    url, headers={"User-Agent": "Mozilla/5.0 (compatible; 5D-Map-Proxy/1.0)"}
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self._set_security_headers()
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                # Log error internally but return generic message
                print(f"Error fetching {url}: {e}")
                msg = b"Upstream Fetch Error"
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

    # Secure binding: Default to localhost, allow override via env var
    host = os.getenv("OWID_PROXY_HOST", "127.0.0.1")

    server = HTTPServer((host, port), ProxyHandler)
    print(f"OWID proxy listening on http://{host}:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

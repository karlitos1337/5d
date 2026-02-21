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
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.send_header("X-Frame-Options", "DENY")

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
                # Add User-Agent to be a good citizen and avoid basic blocking
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "5d-map-proxy/1.0"}
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
                # Log the real error to stderr, don't leak it to client
                sys.stderr.write(f"[ERROR] Proxy fetch failed for {url}: {e}\n")

                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self._set_security_headers()
                self.end_headers()
                self.wfile.write(b"Upstream fetch error")
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self._set_security_headers()
            self.end_headers()
            self.wfile.write(b"Use /proxy/<file>")

    def log_message(self, fmt, *args):
        # Quiet log for requests, errors go to stderr
        pass


def main():
    port = 5510
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    # Default to localhost for security, allow override via env var
    host = os.environ.get("OWID_PROXY_HOST", "127.0.0.1")

    server = HTTPServer((host, port), ProxyHandler)
    print(f"OWID proxy listening on http://{host}:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

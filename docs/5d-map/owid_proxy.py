#!/usr/bin/env python3
import os
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            try:
                key = path.split("/", 1)[1]
            except IndexError:
                self.send_error_response(404, b"Invalid proxy path")
                return

            url = OWID_URLS.get(key)
            if not url:
                self.send_error_response(404, b"Unknown proxy key")
                return

            req = urllib.request.Request(
                url,
                headers={"User-Agent": "OWID-Proxy/1.0"},
            )

            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_security_headers()
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                # Log the actual error to stderr, but send generic error to client
                sys.stderr.write(f"Upstream fetch error: {e}\n")
                self.send_error_response(502, b"Upstream fetch error")
        else:
            self.send_error_response(404, b"Use /proxy/<file>")

    def send_security_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")  # Needed for frontend
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_security_headers()
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message)

    def log_message(self, fmt, *args):
        # Quiet log
        pass


def main():
    port = 5510
    host = os.environ.get("OWID_PROXY_HOST", "127.0.0.1")

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    server = HTTPServer((host, port), ProxyHandler)
    print(f"OWID proxy listening on http://{host}:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

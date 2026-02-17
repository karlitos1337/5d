#!/usr/bin/env python3
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}


class ProxyHandler(BaseHTTPRequestHandler):
    def _send_security_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
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
                self._send_security_headers()
                self.end_headers()
                self.wfile.write(b"Unknown proxy key")
                return
            try:
                with urllib.request.urlopen(url, timeout=15) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self._send_security_headers()
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                # Log error internally but return generic message
                sys.stderr.write(f"Fetch error for {key}: {e}\n")
                msg = b"Fetch error: Internal server error"
                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self._send_security_headers()
                self.end_headers()
                self.wfile.write(msg)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self._send_security_headers()
            self.end_headers()
            self.wfile.write(b"Use /proxy/<file>")

    def log_message(self, fmt, *args):
        # Quiet log
        pass


def main():
    import os
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

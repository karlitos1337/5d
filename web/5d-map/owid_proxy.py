#!/usr/bin/env python3
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}

MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10 MB


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            try:
                parts = path.split("/", 1)
                if len(parts) < 2:
                    raise ValueError("Invalid path")
                key = parts[1]
                url = OWID_URLS.get(key)

                if not url:
                    self.send_response(404)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self._send_security_headers()
                    self.end_headers()
                    self.wfile.write(b"Unknown proxy key")
                    return

                with urllib.request.urlopen(url, timeout=15) as resp:
                    data = bytearray()
                    while True:
                        chunk = resp.read(8192)  # 8KB chunks
                        if not chunk:
                            break
                        data.extend(chunk)
                        if len(data) > MAX_RESPONSE_SIZE:
                            raise ValueError("Response too large")

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self._send_security_headers()
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                # Log to stderr, don't send to client
                print(f"Proxy Error: {e}", file=sys.stderr)

                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self._send_security_headers()
                self.end_headers()

                # Sanitize error message
                if "Response too large" in str(e):
                    msg = b"Error: Response too large"
                else:
                    msg = b"Upstream Fetch Error"
                self.wfile.write(msg)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self._send_security_headers()
            self.end_headers()
            self.wfile.write(b"Use /proxy/<file>")

    def _send_security_headers(self):
        """Helper to send common security and CORS headers."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")

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
    server = HTTPServer(("0.0.0.0", port), ProxyHandler)
    print(f"OWID proxy listening on http://localhost:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}

MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10MB limit


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            try:
                key = path.split("/", 1)[1]
            except IndexError:
                self.send_error_response(400, b"Invalid path format")
                return

            url = OWID_URLS.get(key)
            if not url:
                self.send_error_response(404, b"Unknown proxy key")
                return

            try:
                with urllib.request.urlopen(url, timeout=15) as resp:
                    # Optional: Check Content-Length header first
                    cl = resp.getheader("Content-Length")
                    if cl and int(cl) > MAX_RESPONSE_SIZE:
                        self.send_error_response(502, b"Response too large (header)")
                        return

                    data_chunks = []
                    total_size = 0
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        total_size += len(chunk)
                        if total_size > MAX_RESPONSE_SIZE:
                            self.send_error_response(502, b"Response too large")
                            return
                        data_chunks.append(chunk)

                    data = b"".join(data_chunks)

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                # Log detailed error to stderr (not to user)
                print(f"Proxy error for {url}: {e}", file=sys.stderr)
                self.send_error_response(502, b"Fetch error")
        else:
            self.send_error_response(404, b"Use /proxy/<file>")

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(message)

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

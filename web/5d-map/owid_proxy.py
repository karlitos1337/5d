#!/usr/bin/env python3
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}

# Sentinel: Maximum response size to prevent DoS (10MB)
MAX_RESPONSE_SIZE = 10 * 1024 * 1024


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            key = path.split("/", 1)[1]
            url = OWID_URLS.get(key)
            if not url:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b"Unknown proxy key")
                return

            headers_sent = False
            try:
                with urllib.request.urlopen(url, timeout=15) as resp:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    # Remove Content-Length as we are streaming and might truncate
                    # CORS
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    headers_sent = True

                    total_read = 0
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        total_read += len(chunk)
                        if total_read > MAX_RESPONSE_SIZE:
                            # Sentinel: Abort if too large
                            print(f"⚠️  Response too large ({total_read} > {MAX_RESPONSE_SIZE}), truncating.")
                            break
                        self.wfile.write(chunk)

            except Exception as e:
                print(f"❌ Proxy error: {e}")
                if not headers_sent:
                    self.send_response(502)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(f"Fetch error: {e}".encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
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
    server = HTTPServer(("0.0.0.0", port), ProxyHandler)
    print(f"OWID proxy listening on http://localhost:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

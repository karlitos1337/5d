#!/usr/bin/env python3
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
            key = path.split("/", 1)[1]
            url = OWID_URLS.get(key)
            if not url:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b"Unknown proxy key")
                return
            try:
                # Security: Limit response size to 10MB to prevent DoS via memory exhaustion
                MAX_RESPONSE_SIZE = 10 * 1024 * 1024

                with urllib.request.urlopen(url, timeout=15) as resp:
                    content_length = resp.getheader("Content-Length")
                    if content_length and int(content_length) > MAX_RESPONSE_SIZE:
                        raise ValueError("Response too large (header)")

                    data = b""
                    chunk_size = 8192
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        data += chunk
                        if len(data) > MAX_RESPONSE_SIZE:
                            raise ValueError("Response too large (body)")

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    # CORS
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                msg = f"Fetch error: {e}".encode()
                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(msg)
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

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
                # Security: chunked read with size limit to prevent DoS
                CHUNK_SIZE = 8192

                with urllib.request.urlopen(url, timeout=15) as resp:
                    content_len = resp.getheader("Content-Length")
                    if content_len:
                        try:
                            content_size = int(content_len)
                        except (TypeError, ValueError):
                            # Invalid Content-Length from upstream; log and fall back to streamed size check
                            sys.stderr.write(
                                f"Invalid Content-Length header from upstream for {key}: {content_len}\n"
                            )
                            content_size = -1
                        if content_size > MAX_RESPONSE_SIZE:
                MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10 MB
                CHUNK_SIZE = 8192
                with urllib.request.urlopen(url, timeout=15) as resp:
                    content_len = resp.getheader("Content-Length")
                    if content_len:
                        parsed_len = None
                        try:
                            parsed_len = int(content_len)
                        except (TypeError, ValueError):
                            sys.stderr.write(
                                f"Invalid Content-Length header from upstream for {key}: {content_len}\n"
                            )
                        if parsed_len is not None and parsed_len > MAX_RESPONSE_SIZE:
                            raise ValueError("Response too large")

                    data = b""
                    while True:
                        chunk = resp.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        data += chunk
                        if len(data) > MAX_RESPONSE_SIZE:
                            raise ValueError("Response too large")

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.end_headers()
                    self.wfile.write(data)

            except Exception as e:
                # Log to stderr, don't leak to client
                sys.stderr.write(f"Proxy fetch error for {key}: {e}\n")
                msg = b"Upstream fetch error"
                if "Response too large" in str(e):
                    msg = b"Response too large"

                # Security: Log error internally, return generic message to user
                # print(f"Fetch error for {key}: {e}")  # Internal logging
                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-Content-Type-Options", "nosniff")
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

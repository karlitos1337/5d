#!/usr/bin/env python3
import sys
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}

# 10 MB limit to prevent DoS via memory exhaustion
MAX_RESPONSE_SIZE = 10 * 1024 * 1024


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            key = path.split("/", 1)[1]
            url = OWID_URLS.get(key)
            if not url:
                self.send_response(404)
                self.send_security_headers()
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Unknown proxy key")
                return
            try:
                with urllib.request.urlopen(url, timeout=15) as resp:
                    # Validate content length if available
                    content_length = resp.getheader("Content-Length")
                    if content_length and int(content_length) > MAX_RESPONSE_SIZE:
                        raise ValueError("Response too large (header)")

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_security_headers()
                    # We might not know the full length yet if reading chunked
                    # self.send_header("Content-Length", str(len(data)))
                    # Note: Without Content-Length, client reads until close.

                    self.end_headers()

                    # Read in chunks to avoid memory exhaustion
                    total_size = 0
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        total_size += len(chunk)
                        if total_size > MAX_RESPONSE_SIZE:
                            # We already sent 200 OK, so we can't change status code.
                            # But we can stop sending data and log an error.
                            # The client will get a truncated file, which is safer than crashing server.
                            self.log_error("Response exceeded MAX_RESPONSE_SIZE (%d bytes)", MAX_RESPONSE_SIZE)
                            return
                        self.wfile.write(chunk)

            except Exception as e:
                self.log_error("Fetch error: %s", e)
                # If we haven't sent headers yet, send error
                # If we already started streaming (chunked loop), we can't cleanly send 502.
                # But the try block covers the setup. Once we enter the loop, we are committed.
                # However, exceptions during urlopen() or before send_response() will be caught here.
                try:
                    self.send_response(502)
                    self.send_security_headers()
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.end_headers()
                    # Generic error message to prevent info leak
                    self.wfile.write(b"Upstream request failed")
                except Exception:
                    # Connection might be closed already
                    pass
        else:
            self.send_response(404)
            self.send_security_headers()
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Use /proxy/<file>")

    def send_security_headers(self):
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

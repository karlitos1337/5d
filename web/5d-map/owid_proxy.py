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
                with urllib.request.urlopen(url, timeout=15) as resp:
                    # Security: Check Content-Length header first
                    cl_str = resp.getheader("Content-Length")
                    if cl_str:
                        try:
                            if int(cl_str) > MAX_RESPONSE_SIZE:
                                self.send_error(502, "Upstream response too large (>10MB)")
                                return
                        except ValueError:
                            pass  # Ignore invalid Content-Length

                    # Security: Read in chunks to enforce size limit
                    data = b""
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        data += chunk
                        if len(data) > MAX_RESPONSE_SIZE:
                            self.send_error(502, "Upstream response too large (>10MB)")
                            return

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    # CORS
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                msg = f"Fetch error: {e}".encode()
                # If headers already sent (unlikely here as we buffer), this might fail,
                # but we haven't called send_response yet in the try block logic flow
                # before the exception would occur during read.
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
    # Security: Bind only to localhost to prevent external access
    server = HTTPServer(("127.0.0.1", port), ProxyHandler)
    print(f"OWID proxy listening on http://127.0.0.1:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

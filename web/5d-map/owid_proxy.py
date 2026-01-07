#!/usr/bin/env python3
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}

MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10 MB


class ProxyHandler(BaseHTTPRequestHandler):
    def _send_error_response(self, code, message):
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(message.encode())

    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            key = path.split("/", 1)[1]
            url = OWID_URLS.get(key)
            if not url:
                self._send_error_response(404, "Unknown proxy key")
                return
            try:
                with urllib.request.urlopen(url, timeout=15) as resp:
                    # Check Content-Length if available
                    content_length = resp.info().get("Content-Length")
                    if content_length:
                        try:
                            if int(content_length) > MAX_RESPONSE_SIZE:
                                self._send_error_response(413, "Response too large")
                                return
                        except ValueError:
                            pass  # Ignore invalid Content-Length header

                    # Read in chunks to enforce limit
                    data = bytearray()
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        data.extend(chunk)
                        if len(data) > MAX_RESPONSE_SIZE:
                            self._send_error_response(413, "Response too large")
                            return

                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    # CORS
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                self._send_error_response(502, f"Fetch error: {e}")
        else:
            self._send_error_response(404, "Use /proxy/<file>")

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
    # Bind to 0.0.0.0 to allow container/network access
    server = HTTPServer(("0.0.0.0", port), ProxyHandler)
    print(f"OWID proxy listening on http://0.0.0.0:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

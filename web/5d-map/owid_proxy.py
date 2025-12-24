#!/usr/bin/env python3
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # SECURITY: Only allow specific path prefix
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            try:
                key = path.split("/", 1)[1]
            except IndexError:
                self.send_error(400, "Invalid path")
                return

            url = OWID_URLS.get(key)
            if not url:
                self.send_error(404, "Unknown proxy key")
                return

            try:
                # SECURITY: Set timeout to prevent DoS via hanging connections
                with urllib.request.urlopen(url, timeout=15) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    # CORS: Public data, so * is acceptable here, but be aware.
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                # SECURITY: Log actual error to stderr but don't leak details to client
                self.log_error(f"Fetch error for {key}: {e}")
                self.send_error(502, "Bad Gateway: Upstream fetch failed")
        else:
            self.send_error(404, "Not Found")

    # SECURITY: Removed 'log_message' override to restore default logging to stderr
    # This ensures access logs and errors are visible for auditing.


def main():
    port = 5510
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    # SECURITY: Bind to localhost (127.0.0.1) instead of 0.0.0.0
    # This prevents external access to the proxy.
    bind_address = "127.0.0.1"
    server = HTTPServer((bind_address, port), ProxyHandler)

    print(f"🛡️ OWID proxy secure listening on http://{bind_address}:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

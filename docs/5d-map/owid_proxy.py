#!/usr/bin/env python3
import os
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}


class ProxyHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="text/plain; charset=utf-8"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        # Security Headers
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        # CORS (restrict if needed, but keeping open for local dev convenience)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_HEAD(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            key = path.split("/", 1)[1]
            if key in OWID_URLS:
                self._set_headers(200, "text/csv; charset=utf-8")
            else:
                self._set_headers(404)
        else:
            self._set_headers(404)

    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            key = path.split("/", 1)[1]
            url = OWID_URLS.get(key)
            if not url:
                self._set_headers(404)
                self.wfile.write(b"Unknown proxy key")
                return

            try:
                # Add User-Agent to be polite and avoid blocks
                req = urllib.request.Request(
                    url, headers={"User-Agent": "OWID-Proxy/1.0 (Educational Project)"}
                )

                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))

                    # Security Headers (repeated here because _set_headers ends headers)
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.send_header(
                        "Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'"
                    )
                    self.send_header("X-Frame-Options", "DENY")
                    self.send_header("Referrer-Policy", "no-referrer")
                    self.send_header("Access-Control-Allow-Origin", "*")

                    self.end_headers()
                    self.wfile.write(data)
            except Exception as e:
                # Log full error to stderr, send sanitized error to client
                sys.stderr.write(f"Fetch error for {url}: {e}\n")
                self._set_headers(502)
                self.wfile.write(b"Error fetching upstream resource")
        else:
            self._set_headers(404)
            self.wfile.write(b"Use /proxy/<file>")

    def log_message(self, fmt, *args):
        # Quiet log to avoid cluttering console, unless error
        if args[1].startswith("5") or args[1].startswith("4"):
            sys.stderr.write(
                f"{self.client_address[0]} - - [{self.log_date_time_string()}] {fmt % args}\n"
            )


def main():
    # Default to localhost only for security
    host = os.environ.get("OWID_PROXY_HOST", "127.0.0.1")
    port = 5510

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    server = HTTPServer((host, port), ProxyHandler)
    print(f"🔒 OWID proxy listening on http://{host}:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

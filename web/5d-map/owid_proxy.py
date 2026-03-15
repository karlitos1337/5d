#!/usr/bin/env python3
import os
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OWID_URLS = {
    "depression-prevalence.csv": "https://ourworldindata.org/grapher/depression-prevalence.csv"
}


class ProxyHandler(BaseHTTPRequestHandler):
    def send_security_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Access-Control-Allow-Origin", "*")

    def do_GET(self):
        path = self.path.lstrip("/")
        if path.startswith("proxy/"):
            key = path.split("/", 1)[1]
            url = OWID_URLS.get(key)
            if not url:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_security_headers()
                self.end_headers()
                self.wfile.write(b"Unknown proxy key")
                return
            try:
                # Security: chunked read with size limit to prevent DoS
                MAX_RESPONSE_SIZE = 10 * 1024 * 1024  # 10MB
                CHUNK_SIZE = 8192

                with urllib.request.urlopen(url, timeout=15) as resp:
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.end_headers()

                    total_read = 0
                    while True:
                        chunk = resp.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        total_read += len(chunk)
                        if total_read > MAX_RESPONSE_SIZE:
                            # Log internally, don't leak to client
                            print(f"Error: Response exceeded {MAX_RESPONSE_SIZE} bytes for {key}")
                            return
                        self.wfile.write(chunk)

            except Exception as e:
                # Security: Log error internally, return generic message to user
                # print(f"Fetch error for {key}: {e}")  # Internal logging
                    # MAX_RESPONSE_SIZE = 10MB
                    MAX_RESPONSE_SIZE = 10 * 1024 * 1024
                    chunks = []
                    total_size = 0
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        chunks.append(chunk)
                        total_size += len(chunk)
                        if total_size > MAX_RESPONSE_SIZE:
                            self.send_response(502)
                            self.send_header("Content-Type", "text/plain; charset=utf-8")
                            self.send_header("Access-Control-Allow-Origin", "*")
                            self.send_header("X-Content-Type-Options", "nosniff")
                            self.end_headers()
                            self.wfile.write(b"Response too large")
                            return

                    content = b"".join(chunks)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(content)))
                    # CORS
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.send_header("X-Content-Type-Options", "nosniff")
                    self.end_headers()
                    self.wfile.write(content)
            except Exception:
                # Log error securely (not exposing to user)
                msg = b"Fetch error: Upstream Service Error"
                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("X-Content-Type-Options", "nosniff")
                req = urllib.request.Request(url, headers={"User-Agent": "OWID-Proxy/1.0"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = resp.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_security_headers()
                    self.end_headers()
                    self.wfile.write(data)
            except Exception:
                # Log error locally if needed, but don't send to client
                msg = b"Upstream fetch error"
                self.send_response(502)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_security_headers()
                self.end_headers()
                self.wfile.write(b"Upstream fetch error")
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_security_headers()
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

    host = os.environ.get("OWID_PROXY_HOST", "127.0.0.1")
    server = HTTPServer((host, port), ProxyHandler)
    print(f"OWID proxy listening on http://{host}:{port}/proxy/<file>")
    print("Supported keys:", ", ".join(OWID_URLS.keys()))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

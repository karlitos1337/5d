import http.server
import os
import socketserver
import urllib.error
import urllib.request

PORT = 5510
HOST = os.environ.get('OWID_PROXY_HOST', '127.0.0.1')

# Allow CORS and Security Headers
class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'")
        self.send_header('X-Frame-Options', 'DENY')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/proxy/'):
            # Extract filename from path
            filename = self.path.split('/')[-1]
            # Map filenames to OWID URLs
            url_map = {
                'depression-prevalence.csv': 'https://ourworldindata.org/grapher/depression-prevalence.csv?v=1&csvType=full&useColumnShortNames=true',
                # Add more mappings as needed
            }

            target_url = url_map.get(filename)

            if target_url:
                try:
                    # Fetch from OWID with timeout and User-Agent
                    req = urllib.request.Request(
                        target_url,
                        headers={'User-Agent': 'Mozilla/5.0 (5d-map-proxy)'}
                    )
                    with urllib.request.urlopen(req, timeout=15) as response:
                        content = response.read()

                    self.send_response(200)
                    self.send_header('Content-type', 'text/csv')
                    self.end_headers()
                    self.wfile.write(content)
                except Exception as e:
                    self.send_error(500, f"Proxy error: {str(e)}")
            else:
                self.send_error(404, "File not found in proxy map")
        else:
            self.send_error(403, "Forbidden")

if __name__ == "__main__":
    print(f"Starting OWID Proxy on {HOST}:{PORT}...")
    # Bind to localhost only for security
    with socketserver.TCPServer((HOST, PORT), CORSRequestHandler) as httpd:
        print(f"Proxy running. Access via http://{HOST}:{PORT}/proxy/depression-prevalence.csv")
        httpd.serve_forever()

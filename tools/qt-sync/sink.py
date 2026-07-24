"""Tiny localhost sink: receives one POST body and writes it to a file.

Used by the harvest step: the in-app browser can reach Etsy (DataDome passes
a real browser) but can't write files; Python can write files but can't reach
Etsy (curl/urllib get HTTP 403). So the browser fetches the shop pages and
POSTs the harvested JSON here.

Usage: python sink.py <out_path> [port]   (default port 8377)
Exits after receiving one POST (or after 120s timeout).
"""
import sys, json
from http.server import BaseHTTPRequestHandler, HTTPServer

out_path = sys.argv[1]
port = int(sys.argv[2]) if len(sys.argv) > 2 else 8377

class H(BaseHTTPRequestHandler):
    got = False
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        json.loads(body.decode('utf-8'))  # validate it parses before saving
        with open(out_path, 'wb') as f:
            f.write(body)
        self.send_response(200); self.end_headers(); self.wfile.write(b'ok')
        H.got = True
    def do_OPTIONS(self):  # CORS preflight, just in case
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.end_headers()
    def log_message(self, *a):  # quiet
        pass

srv = HTTPServer(('127.0.0.1', port), H)
srv.timeout = 120
while not H.got:
    srv.handle_request()
print('saved', out_path)

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen

N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL', 'http://n8n:5678/webhook/discrepancy-intake')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":"ok"}'); return
        self.send_error(404)

    def do_POST(self):
        if self.path != '/events': self.send_error(404); return
        body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
        # A Kafka consumer should call this handler with the decoded event.
        request = Request(N8N_WEBHOOK_URL, data=body, headers={'Content-Type': 'application/json'})
        try:
            with urlopen(request, timeout=10) as response: status = response.status
            self.send_response(202 if status < 300 else 502)
        except Exception:
            self.send_response(202)  # keep local demo ingestion non-blocking
        self.end_headers()

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8081), Handler).serve_forever()

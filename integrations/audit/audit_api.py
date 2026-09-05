import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from sheets_writer import write_audit

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health': self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":"ok"}'); return
        self.send_error(404)
    def do_POST(self):
        if self.path != '/audit': self.send_error(404); return
        try:
            record = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))))
            write_audit(record, os.getenv('AUDIT_PATH', '/data/audit.csv'))
            self.send_response(201); self.end_headers(); self.wfile.write(b'{"status":"recorded"}')
        except Exception as exc:
            self.send_response(400); self.end_headers(); self.wfile.write(json.dumps({'error': str(exc)}).encode())

if __name__ == '__main__': HTTPServer(('0.0.0.0', 8090), Handler).serve_forever()

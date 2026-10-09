import http.server
import socketserver
import os
import sys
import mimetypes

PORT = 7575
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

# Colors
G = '\033[32m'; R = '\033[31m'; Y = '\033[33m'
C = '\033[36m'; M = '\033[35m'; D = '\033[90m'; X = '\033[0m'

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silence default logging

    def do_GET(self):
        import time
        start = time.time()
        path = self.path.split('?')[0]
        if path == '/':
            path = '/index.html'

        file_path = os.path.join(ROOT, path.lstrip('/'))

        if not os.path.abspath(file_path).startswith(ROOT) or not os.path.isfile(file_path):
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = f'''<html><body style="background:#030712;color:#fff;font-family:sans-serif;text-align:center;padding:60px">
            <h1 style="color:#a855f7">404 — Not Found</h1>
            <p><code>{path}</code> does not exist</p>
            <a href="/" style="color:#a855f7">← Go home</a>
            </body></html>'''
            self.wfile.write(html.encode())
            print(f'{R}✗ 404{X} {path} ({(time.time()-start)*1000:.0f}ms)')
            return

        mime, _ = mimetypes.guess_type(file_path)
        if not mime:
            mime = 'application/octet-stream'
        if mime.startswith('text/') or mime in ('application/javascript', 'application/json'):
            mime += '; charset=utf-8'

        size = os.path.getsize(file_path)

        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(size))
        self.end_headers()

        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())

        kb = size / 1024
        color = Y if size > 100000 else G
        print(f'{color}✓ 200{X} {path} {kb:.1f}KB ({(time.time()-start)*1000:.0f}ms)')

class ReusableServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

print(f'\n{M}🎌  AniPulse Dev Server{X}')
print(f'{D}─────────────────────────────{X}')
print(f'  {G}➜{X}  Local:   {C}http://localhost:{PORT}{X}')
print(f'  {D}📁 Root: {ROOT}{X}')
print(f'  {D}⏹  Stop: Ctrl + C{X}\n')

try:
    with ReusableServer(('', PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print(f'\n{M}👋 Server stopped{X}\n')
    sys.exit(0)

"""家庭收纳管理 - 轻量服务器
启动后电脑和手机都能访问，数据保存在服务器端。
用法：python server.py
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, os, socket, urllib.parse, hashlib

PORT = int(os.environ.get('PORT', 8080))
DATA_FILE = 'storage_data.json'
AUTH_FILE = 'auth_hash.json'
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))


def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def hash_code(code):
    return hashlib.sha256(code.encode('utf-8')).hexdigest()


def get_saved_hash():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, 'r') as f:
            return json.load(f).get('hash', '')
    return ''


def save_hash(h):
    with open(AUTH_FILE, 'w') as f:
        json.dump({'hash': h}, f)


class Handler(SimpleHTTPRequestHandler):

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == '/api/data':
            data = {}
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            self._json_response(data)
            return

        # Serve HTML for all other paths (SPA routing)
        if path in ('', '/') or not os.path.isfile(os.path.join(STATIC_DIR, path.lstrip('/'))):
            self.path = '/家庭收纳管理.html'
        super().do_GET()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path

        if path == '/api/auth':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                req = json.loads(body)
                code = req.get('code', '').strip()
                if not code:
                    self._json_response({'error': '请输入密码'}, 400)
                    return
                saved = get_saved_hash()
                if not saved:
                    # First time: set password
                    h = hash_code(code)
                    save_hash(h)
                    self._json_response({'ok': True, 'new': True})
                elif hash_code(code) == saved:
                    self._json_response({'ok': True})
                else:
                    self._json_response({'error': '密码错误'}, 403)
            except Exception as e:
                self._json_response({'error': str(e)}, 400)
            return

        if path == '/api/data':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                if 'locations' not in data or not isinstance(data['locations'], list):
                    self._json_response({'error': '数据格式错误'}, 400)
                    return
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self._json_response({'ok': True})
            except Exception as e:
                self._json_response({'error': str(e)}, 400)
            return

        self.send_error(404)

    def _json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f'[{self.log_date_time_string()}] {format % args}')


if __name__ == '__main__':
    lan_ip = get_lan_ip()
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'{"=" * 50}')
    print(f'  家庭收纳管理服务器已启动！')
    print()
    print(f'  本机访问：http://localhost:{PORT}')
    print(f'  局域网：  http://{lan_ip}:{PORT}')
    print(f'  （手机连同一WiFi后扫码或输入局域网地址）')
    print(f'{"=" * 50}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止')
        server.server_close()

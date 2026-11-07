# -*- coding: utf-8 -*-
"""
Локальный и production-like сервер: статика + POST /api/callback.
Запуск: py -3 server/app.py
Переменные: PORT, BIND_HOST (0.0.0.0 на сервере), .env с SMTP/webhook.
"""
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from callback_api import MAX_BODY_BYTES, client_ip, handle_callback_json, load_dotenv

ROOT = Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path.split("?")[0] != "/api/callback":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY_BYTES:
            self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"ok": False, "message": "Слишком большой запрос."})
            return
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Неверный JSON"})
            return

        ip = client_ip(dict(self.headers), self.client_address)
        status, payload = handle_callback_json(data, ip=ip)
        self._json(status, payload)

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


def main():
    import os

    load_dotenv()
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get("BIND_HOST", "127.0.0.1").strip() or "127.0.0.1"
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Serving {ROOT} at http://{host}:{port}/")
    print("POST /api/callback — заявки на звонок")
    if host == "127.0.0.1":
        print("Для проверки формы откройте этот адрес, не Live Server без прокси.")
    server.serve_forever()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
WSGI-обёртка для gunicorn / waitress (только API; статику отдаёт nginx).

Пример:
  waitress-serve --listen=127.0.0.1:8081 server.wsgi:application

nginx раздаёт файлы сайта и проксирует location /api/callback сюда.
"""
import json
from callback_api import MAX_BODY_BYTES, handle_callback_json, load_dotenv

load_dotenv()


def _json_response(start_response, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ]
    start_response(status, headers)
    return [body]


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "")
    if method == "POST" and path.rstrip("/") == "/api/callback":
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
        except ValueError:
            length = 0
        if length > MAX_BODY_BYTES:
            return _json_response(start_response, "413 Payload Too Large", {"ok": False, "message": "Слишком большой запрос."})
        raw = environ["wsgi.input"].read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return _json_response(start_response, "400 Bad Request", {"ok": False, "message": "Неверный JSON"})
        ip = environ.get("REMOTE_ADDR", "unknown")
        if environ.get("HTTP_X_FORWARDED_FOR"):
            ip = environ["HTTP_X_FORWARDED_FOR"].split(",")[0].strip()
        http_status, payload = handle_callback_json(data, ip=ip)
        return _json_response(start_response, f"{http_status.value} {http_status.phrase}", payload)
    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Not found"]

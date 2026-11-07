# -*- coding: utf-8 -*-
"""
Локальный сервер: статика сайта + POST /api/callback.
Запуск из корня проекта: py -3 server/app.py
"""
import json
import os
import re
import smtplib
import urllib.error
import urllib.request
from datetime import datetime, timezone
from email.message import EmailMessage
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "server" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_dotenv():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def valid_phone(digits: str) -> bool:
    if len(digits) == 11 and digits[0] in "78":
        return True
    if len(digits) == 10 and digits[0] == "9":
        return True
    return False


def deliver(name: str, phone: str):
    """Возвращает (ok, code, message)."""
    webhook = os.environ.get("CALLBACK_WEBHOOK_URL", "").strip()
    smtp_host = os.environ.get("SMTP_HOST", "").strip()
    smtp_to = os.environ.get("CALLBACK_EMAIL_TO", "").strip() or os.environ.get("SMTP_TO", "").strip()

    body = f"Обратный звонок с сайта КФХ Малышева\nИмя: {name}\nТелефон: +{phone if phone.startswith('7') else phone}\nВремя: {datetime.now(timezone.utc).isoformat()}\n"

    if webhook:
        payload = json.dumps({"name": name, "phone": phone, "source": "kfh-site"}).encode("utf-8")
        req = urllib.request.Request(
            webhook,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status >= 400:
                return False, "WEBHOOK_FAILED", f"Webhook вернул {resp.status}"
        return True, "OK", "sent"

    if smtp_host and smtp_to:
        port = int(os.environ.get("SMTP_PORT", "587"))
        user = os.environ.get("SMTP_USER", "")
        password = os.environ.get("SMTP_PASSWORD", "")
        mail_from = os.environ.get("SMTP_FROM", user or smtp_to)
        msg = EmailMessage()
        msg["Subject"] = "Заявка на обратный звонок — КФХ Малышева"
        msg["From"] = mail_from
        msg["To"] = smtp_to
        msg.set_content(body)
        with smtplib.SMTP(smtp_host, port, timeout=20) as smtp:
            if os.environ.get("SMTP_TLS", "1") == "1":
                smtp.starttls()
            if user and password:
                smtp.login(user, password)
            smtp.send_message(msg)
        return True, "OK", "sent"

    # журнал, если канал не настроен — НЕ считаем успехом для клиента
    log_path = DATA_DIR / "callbacks.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"name": name, "phone": phone, "ts": datetime.now(timezone.utc).isoformat()}, ensure_ascii=False) + "\n")
    return False, "NOT_CONFIGURED", "Канал доставки не настроен (SMTP или CALLBACK_WEBHOOK_URL)."


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path.split("?")[0] != "/api/callback":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Неверный JSON"})
            return

        name = str(data.get("name", "")).strip()
        phone = re.sub(r"\D", "", str(data.get("phone", "")))
        if phone.startswith("8") and len(phone) == 11:
            phone = "7" + phone[1:]
        if len(phone) == 10:
            phone = "7" + phone

        if len(name) < 2:
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Укажите имя."})
            return
        if not valid_phone(phone):
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Неверный номер телефона."})
            return
        if not data.get("consent"):
            self._json(HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Нужно согласие на обработку данных."})
            return

        ok, code, _msg = deliver(name, phone)
        if ok:
            self._json(HTTPStatus.OK, {"ok": True})
        else:
            status = HTTPStatus.SERVICE_UNAVAILABLE if code == "NOT_CONFIGURED" else HTTPStatus.BAD_GATEWAY
            self._json(status, {"ok": False, "code": code, "message": _msg})

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
    load_dotenv()
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Serving {ROOT} at http://127.0.0.1:{port}/")
    print("POST /api/callback — заявки на звонок")
    server.serve_forever()


if __name__ == "__main__":
    main()

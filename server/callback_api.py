# -*- coding: utf-8 -*-
"""Обработка POST /api/callback — валидация, антиспам, доставка."""
import json
import os
import re
import smtplib
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from email.message import EmailMessage
from http import HTTPStatus
from pathlib import Path
from threading import Lock

ROOT = Path(__file__).resolve().parents[1]
MAX_BODY_BYTES = 4096
RATE_WINDOW_SEC = 900
RATE_MAX_PER_IP = 8

_rate: dict[str, list[float]] = defaultdict(list)
_rate_lock = Lock()


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


def client_ip(headers: dict, client_address) -> str:
    fwd = headers.get("X-Forwarded-For") or headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    return client_address[0] if client_address else "unknown"


def rate_limit_ok(ip: str) -> bool:
    now = time.time()
    with _rate_lock:
        bucket = _rate[ip]
        bucket[:] = [t for t in bucket if now - t < RATE_WINDOW_SEC]
        if len(bucket) >= RATE_MAX_PER_IP:
            return False
        bucket.append(now)
        return True


def deliver(name: str, phone: str):
    """Возвращает (ok, code, message)."""
    webhook = os.environ.get("CALLBACK_WEBHOOK_URL", "").strip()
    smtp_host = os.environ.get("SMTP_HOST", "").strip()
    smtp_to = os.environ.get("CALLBACK_EMAIL_TO", "").strip() or os.environ.get("SMTP_TO", "").strip()

    body = (
        f"Обратный звонок с сайта КФХ Малышева\n"
        f"Имя: {name}\n"
        f"Телефон: +{phone if phone.startswith('7') else phone}\n"
        f"Время: {datetime.now(timezone.utc).isoformat()}\n"
    )

    if webhook:
        payload = json.dumps({"name": name, "phone": phone, "source": "kfh-site"}).encode("utf-8")
        req = urllib.request.Request(
            webhook,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status >= 400:
                    return False, "WEBHOOK_FAILED", f"Webhook вернул {resp.status}"
        except urllib.error.URLError as e:
            return False, "WEBHOOK_FAILED", f"Ошибка webhook: {e}"
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
        try:
            with smtplib.SMTP(smtp_host, port, timeout=20) as smtp:
                if os.environ.get("SMTP_TLS", "1") == "1":
                    smtp.starttls()
                if user and password:
                    smtp.login(user, password)
                smtp.send_message(msg)
        except smtplib.SMTPException as e:
            return False, "SMTP_FAILED", f"Ошибка почты: {e}"
        return True, "OK", "sent"

    return False, "NOT_CONFIGURED", "Канал доставки не настроен (SMTP или CALLBACK_WEBHOOK_URL)."


def handle_callback_json(data: dict, *, ip: str):
    """
    Обрабатывает уже распарсенный JSON.
    Возвращает (http_status: int, payload: dict).
    """
    if data.get("website"):
        return HTTPStatus.OK, {"ok": True}

    if not rate_limit_ok(ip):
        return HTTPStatus.TOO_MANY_REQUESTS, {
            "ok": False,
            "code": "RATE_LIMIT",
            "message": "Слишком много запросов. Позвоните по телефону или попробуйте позже.",
        }

    name = str(data.get("name", "")).strip()[:120]
    phone = re.sub(r"\D", "", str(data.get("phone", "")))[:11]
    if phone.startswith("8") and len(phone) == 11:
        phone = "7" + phone[1:]
    if len(phone) == 10:
        phone = "7" + phone

    if len(name) < 2:
        return HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Укажите имя."}
    if not valid_phone(phone):
        return HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Неверный номер телефона."}
    if not data.get("consent"):
        return HTTPStatus.BAD_REQUEST, {"ok": False, "message": "Нужно согласие на обработку данных."}

    ok, code, msg = deliver(name, phone)
    if ok:
        return HTTPStatus.OK, {"ok": True}
    status = HTTPStatus.SERVICE_UNAVAILABLE if code == "NOT_CONFIGURED" else HTTPStatus.BAD_GATEWAY
    return status, {"ok": False, "code": code, "message": msg}

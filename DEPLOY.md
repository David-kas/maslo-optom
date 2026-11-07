# Публикация сайта и форма обратного звонка

Сайт — **статические HTML** (сборка `py -3 tools/build_site.py`) плюс **один API** `POST /api/callback`.

## Важно

- Открытие файлов через **Live Server** (`127.0.0.1:5500`) **не** обслуживает `/api/callback` — форма вернёт ошибку. Это нормально.
- Для проверки формы локально: `py -3 server/app.py` → `http://127.0.0.1:8080/`.
- На боевом домене нужен **либо** Python/WSGI за nginx, **либо** прокси на тот же endpoint.

## Переменные окружения (`.env` в корне)

Обязательно настройте **один** канал доставки:

| Переменная | Назначение |
|------------|------------|
| `CALLBACK_WEBHOOK_URL` | POST JSON `{name, phone, source}` в CRM/бот |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` | Почта |
| `CALLBACK_EMAIL_TO` | Куда слать заявки |
| `PORT` | Порт (по умолчанию 8080) |
| `BIND_HOST` | `127.0.0.1` локально, `0.0.0.0` на VPS при прокси nginx |

Без webhook и SMTP клиент увидит: *«Отправка не настроена»* — **без** фальшивого успеха. Заявки **не** пишутся в файлы на диск.

## Вариант A: один сервер Python (VPS)

```text
BIND_HOST=0.0.0.0 PORT=8080
py -3 server/app.py
```

Перед ним — nginx с TLS, раздача статики из корня проекта и при необходимости прокси только `/api/callback`.

## Вариант B: nginx + waitress (рекомендуется)

```bash
pip install waitress
waitress-serve --listen=127.0.0.1:8081 server.wsgi:application
```

Пример фрагмента nginx:

```nginx
location /api/callback {
    proxy_pass http://127.0.0.1:8081;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    client_max_body_size 8k;
}
location / {
    root /var/www/maslohoz64;
    try_files $uri $uri/ =404;
}
```

## Защита API

- Лимит запросов с одного IP (встроено в `server/callback_api.py`).
- Honeypot-поле `website` (скрытое) — тихий ответ без доставки.
- Максимальный размер тела запроса 4 КБ.

## После деплоя

1. Заполните `.env` на сервере (не коммитьте в git).
2. Отправьте тестовую заявку с страницы контактов.
3. Проверьте `py -3 tools/verify_site.py` на собранных файлах.

Юридический текст политики ПДн и сроки хранения заявок — см. `OWNER-QUESTIONS.md`.

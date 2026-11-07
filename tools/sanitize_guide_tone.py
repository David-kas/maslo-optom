# -*- coding: utf-8 -*-
"""Убираем мета-формулировки «справочник / 10k слов / CMS» из home_guide.md."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "content" / "home_guide.md"

DROP_PARAGRAPH_STARTS = (
    "Если вы готовите внутреннее согласование",
    "Для аудита со стороны головной компании",
    "Наконец, если ваша организация ведёт публичные тендеры",
    "При импорте этого текста в вашу CMS",
    "**Расширенный контекст для закупщика (уникальные тезисы).**",
)

SUBS = [
    (re.compile(r"в открытом справочнике", re.I), "публично на сайте"),
    (re.compile(r"справочник не подтверждает", re.I), "детали уточняют у менеджера"),
    (re.compile(r"справочник не утверждает", re.I), "это зона ответственности покупателя"),
    (re.compile(r"справочник не содержит", re.I), "цифры не публикуются"),
    (re.compile(r"справочник не подменяет", re.I), "текст не заменяет"),
    (re.compile(r"справочник не является", re.I), "сайт не является"),
    (re.compile(r"справочник не публикует", re.I), "на сайте не публикуют"),
    (re.compile(r"справочник подчёркивает:", re.I), "важно:"),
    (re.compile(r"Формулировка справочника остаётся жёсткой:", re.I), "Важно:"),
    (re.compile(r"не полагаясь только на этот справочник", re.I), "— уточните у менеджера"),
    (re.compile(r"в справочник не включены:", re.I), "не выкладываем в открытую:"),
    (re.compile(r"Честный B2B-справочник перечисляет", re.I), "Кратко о границах:"),
    (re.compile(r"\*\*не гарантия справочника\*\*", re.I), "**по документам партии**"),
    (re.compile(r"оглавления сайта", re.I), "договора"),
    (re.compile(r"на момент чтения справочника", re.I), "сейчас"),
    (re.compile(r"Частые вопросы в справочнике", re.I), "Частые вопросы"),
    (re.compile(r"в справочнике", re.I), "на сайте"),
    (re.compile(r"справочник \*\*не утверждает\*\*", re.I), "мы **не фиксируем**"),
    (re.compile(r"справочник намеренно не фиксирует", re.I), "на сайте не фиксируем"),
    (re.compile(r"В данном справочнике", re.I), "Здесь"),
    (re.compile(r"Справочник \*\*не является гарантией\*\*", re.I), "**Сайт не гарантирует**"),
    (re.compile(r"обязательство справочника", re.I), "обещание в рекламе"),
    (re.compile(r"не гарантируется справочником", re.I), "оформляется в договоре"),
    (re.compile(r"Справочник обновляют при смене фактов на сайте; договор важнее справочника\.", re.I), "Актуальные условия — в договоре и письмах менеджера."),
    (re.compile(r"не указанное поимённо в справочнике", re.I), "— уточняйте по телефону"),
    (re.compile(r"на момент подготовки справочника", re.I), "сейчас"),
]


def main():
    text = MD.read_text(encoding="utf-8")
    lines = text.splitlines()
    out = []
    skip_para = False
    for line in lines:
        stripped = line.strip()
        if any(stripped.startswith(p) for p in DROP_PARAGRAPH_STARTS):
            skip_para = True
            continue
        if skip_para:
            if not stripped:
                skip_para = False
            continue
        out.append(line)
    text = "\n".join(out)
    for pat, repl in SUBS:
        text = pat.sub(repl, text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    MD.write_text(text.rstrip() + "\n", encoding="utf-8")
    print("Sanitized", MD)


if __name__ == "__main__":
    main()

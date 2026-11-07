# -*- coding: utf-8 -*-
"""Полная пересборка content/home_guide.md."""
from __future__ import annotations

import pathlib
import re

from guide_chunks import CHUNKS, FAQ, GLOSSARY, CLOSING

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "home_guide.md"

HEADER = """# Справочник для оптовых покупателей: КФХ Малышева — подсолнечное масло и жмых

Этот материал адресован специалистам по закупкам в АПК: технологам комбикормовых заводов, кормовикам молочных и мясных комплексов, снабженцам птицефабрик, закупщикам пищевых производств и переработчиков масла. В тексте — только подтверждённые сведения о продукции, таре, услугах и контактах КФХ Малышева в Прихопёрье, Саратовская область. Коммерческие цены, перечень действующих сертификатов на будущие партии, экспортная история по отдельным странам и любые лабораторные «гарантии» сверх документов конкретной партии в справочник не включены: их согласуют с менеджером по запросу.

Девиз: **«Трудимся во благо людей с 2007 года»**.

## id-oglavlenie {#id-oglavlenie}

- О предприятии и реквизитах
- Прихопёрье, адрес и координаты завода
- Выращивание подсолнечника
- Прессовый отжим и переработка
- Масло I сорта: ГОСТ 1129-2013, HS 1512.11
- Жмых: ГОСТ 80-96, HS 2306.30, ракушка и дроблёный
- Упаковка и минимальная партия масла
- Логистика и доставка
- Закупка семян
- Давальческая переработка
- Качество и документы на партию
- Покупатели: кормовой и пищевой сегмент
- География поставок (для обсуждения)
- Планы развития производства
- Вопросы и ответы
- Глоссарий
- Как запросить коммерческое предложение"""


def word_count(text: str) -> int:
    return len(re.findall(r"[\w\u0400-\u04FF]+", text))


def main() -> None:
    faq_lines = ["## id-voprosy-i-otvety {#id-voprosy-i-otvety}", ""]
    for n, (q, a) in enumerate(FAQ, 1):
        faq_lines.extend([f"### vopros-{n}", "", f"**{q}**", "", a, ""])
    gloss_lines = ["## id-glossariy {#id-glossariy}", ""]
    for term, definition in GLOSSARY:
        gloss_lines.extend([f"**{term}** — {definition}", ""])
    text = "\n\n".join(
        [HEADER, "\n\n".join(CHUNKS), "\n".join(faq_lines), "\n".join(gloss_lines), CLOSING]
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print("words", word_count(text))


if __name__ == "__main__":
    main()

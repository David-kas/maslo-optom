# -*- coding: utf-8 -*-
"""Дополняет content/home_guide.md уникальными блоками до >=10000 слов."""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MD = ROOT / "content" / "home_guide.md"

# Импортируем крупные текстовые блоки из соседнего модуля
from guide_chunks import CHUNKS, FAQ, GLOSSARY, CLOSING  # noqa: E402


def word_count(text: str) -> int:
    return len(re.findall(r"[\w\u0400-\u04FF]+", text))


def main() -> None:
    body = MD.read_text(encoding="utf-8")
    if "PLACEHOLDER_EXPAND" not in body:
        raise SystemExit("placeholder missing")
    insert = "\n\n".join(CHUNKS)
    faq_lines = ["## id-voprosy-i-otvety {#id-voprosy-i-otvety}", ""]
    for n, (q, a) in enumerate(FAQ, 1):
        faq_lines.append(f"### vopros-{n}")
        faq_lines.append("")
        faq_lines.append(f"**{q}**")
        faq_lines.append("")
        faq_lines.append(a)
        faq_lines.append("")
    gloss_lines = ["## id-glossariy {#id-glossariy}", ""]
    for term, definition in GLOSSARY:
        gloss_lines.append(f"**{term}** — {definition}")
        gloss_lines.append("")
    replacement = "\n\n".join(
        [insert, "\n".join(faq_lines), "\n".join(gloss_lines), CLOSING]
    )
    out = body.replace("PLACEHOLDER_EXPAND", replacement)
    MD.write_text(out, encoding="utf-8")
    print("words", word_count(out))


if __name__ == "__main__":
    main()

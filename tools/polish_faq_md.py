# -*- coding: utf-8 -*-
"""Правка ответов FAQ в content/home_guide.md."""
import re
from pathlib import Path

from faq_guide import polish_answer

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "content" / "home_guide.md"
INTRO = (
    "\n\nНиже — коротко о поставках масла и жмыха. Цены, остатки и комплект документов на конкретную дату "
    "даём в коммерческом предложении: оставьте заявку на звонок или напишите на почту.\n"
)


def main():
    text = MD.read_text(encoding="utf-8")
    lines = text.splitlines()
    out = []
    in_faq = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^##\s+id-voprosy-i-otvety\b", line, re.I):
            in_faq = True
            out.append(line)
            if INTRO.strip() not in text:
                out.append(INTRO.rstrip())
            i += 1
            continue
        if in_faq and line.startswith("## "):
            in_faq = False
        if in_faq and re.match(r"^###\s+vopros-\d+\s*$", line, re.I):
            out.append(line)
            i += 1
            while i < len(lines) and not lines[i].strip():
                out.append(lines[i])
                i += 1
            if i < len(lines):
                out.append(lines[i])
                i += 1
            while i < len(lines) and not lines[i].strip():
                out.append(lines[i])
                i += 1
            while i < len(lines) and not re.match(r"^#{1,6}\s", lines[i]):
                if lines[i].startswith("**"):
                    out.append(lines[i])
                else:
                    out.append(polish_answer(lines[i]))
                i += 1
            continue
        out.append(line)
        i += 1
    MD.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("Updated", MD)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Парсинг блока FAQ в home_guide.md."""
import re

FAQ_SECTION = "id-voprosy-i-otvety"


def polish_answer(text: str) -> str:
    """Лёгкая правка без ломания смысла (основная редактура — в home_guide.md)."""
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    if t and t[-1] not in ".!?":
        t += "."
    return t


def iter_faq_pairs(md: str):
    """Пары (вопрос, ответ) из секции id-voprosy-i-otvety."""
    lines = md.splitlines()
    in_faq = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^##\s+id-voprosy-i-otvety\b", line, re.I):
            in_faq = True
            i += 1
            continue
        if in_faq and re.match(r"^##\s+", line):
            break
        if in_faq and re.match(r"^###\s+vopros-\d+\s*$", line, re.I):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i >= len(lines):
                break
            qm = re.match(r"^\*\*(.+?)\*\*\s*$", lines[i])
            if not qm:
                i += 1
                continue
            question = qm.group(1).strip()
            i += 1
            paras = []
            while i < len(lines):
                if re.match(r"^#{1,6}\s", lines[i]):
                    break
                if lines[i].strip():
                    paras.append(lines[i].strip())
                elif paras:
                    break
                i += 1
            answer = polish_answer(" ".join(paras))
            yield question, answer
            continue
        i += 1


def faq_json_ld_from_guide(md: str, limit: int = 15):
    entities = []
    for q, a in iter_faq_pairs(md):
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
        if len(entities) >= limit:
            break
    if not entities:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }

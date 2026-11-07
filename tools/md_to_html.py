# -*- coding: utf-8 -*-
import html
import re

from faq_guide import polish_answer
from heading_titles import title_for_slug

FAQ_CHAPTER = "id-voprosy-i-otvety"


def slugify_heading(text):
    m = re.match(r"^(id-[a-z0-9-]+)", text.strip(), re.I)
    if m:
        return m.group(1).lower()
    base = re.sub(r"[^a-z0-9а-яё-]+", "-", text.lower())
    return re.sub(r"-+", "-", base).strip("-")


def inline_md(escaped: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def _read_faq_item(lines, i):
    """После строки ### vopros-N возвращает (question, answer_html, next_i)."""
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return None, "", i
    qm = re.match(r"^\*\*(.+?)\*\*\s*$", lines[i])
    if not qm:
        return None, "", i
    question = qm.group(1).strip()
    i += 1
    paras = []
    while i < len(lines):
        if re.match(r"^#{1,6}\s", lines[i]):
            break
        if lines[i].startswith("- "):
            break
        if lines[i].strip():
            paras.append(polish_answer(lines[i].strip()))
        elif paras:
            break
        i += 1
    answer = " ".join(paras)
    body = f"<p>{inline_md(html.escape(answer))}</p>" if answer else ""
    return question, body, i


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_ul = False
    chapter_open = False
    current_chapter = ""
    faq_list_open = False
    i = 0
    skip_title = True  # первый # заголовок — служебный

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def close_faq_list():
        nonlocal faq_list_open
        if faq_list_open:
            out.append("</div>")
            faq_list_open = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("# ") and skip_title:
            i += 1
            skip_title = False
            continue
        if re.match(r"^#{1,6}\s", line):
            close_ul()
            level = len(re.match(r"^(#+)", line).group(1))
            raw = re.sub(r"^#+\s*", "", line).strip()
            raw = re.sub(r"\s*\{#.*\}\s*$", "", raw)
            sid = slugify_heading(raw)

            if level == 3 and current_chapter == FAQ_CHAPTER and re.match(r"^vopros-\d+$", raw, re.I):
                vm = re.match(r"^vopros-(\d+)$", raw, re.I)
                i += 1
                question, answer_html, i = _read_faq_item(lines, i)
                if question:
                    if not faq_list_open:
                        out.append('<div class="faq-list faq-list--guide">')
                        faq_list_open = True
                    fid = f"faq-vopros-{vm.group(1)}" if vm else "faq-item"
                    out.append(
                        f'<details class="faq-item" id="{html.escape(fid)}">'
                        f"<summary>{html.escape(question)}</summary>{answer_html}</details>"
                    )
                continue

            if level <= 2:
                close_faq_list()
                if chapter_open:
                    out.append("</section>")
                if sid == "id-oglavlenie":
                    i += 1
                    while i < len(lines):
                        if re.match(r"^##\s+", lines[i]):
                            break
                        i += 1
                    chapter_open = False
                    current_chapter = ""
                    continue
                title = title_for_slug(sid, raw)
                current_chapter = sid if level == 2 else current_chapter
                out.append(
                    f'<section class="guide-chapter" aria-labelledby="{html.escape(sid)}">'
                    f'<h2 id="{html.escape(sid)}">{html.escape(title)}</h2>'
                )
                chapter_open = True
            else:
                title = title_for_slug(sid, raw)
                if not re.match(r"^vopros-\d+$", raw, re.I):
                    out.append(f"<h3>{html.escape(title)}</h3>")
            i += 1
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(html.escape(line[2:].strip()))}</li>")
            i += 1
            continue
        if not line.strip():
            close_ul()
            i += 1
            continue
        close_ul()
        para = []
        while i < len(lines):
            s = lines[i]
            if not s.strip():
                break
            if re.match(r"^#{1,6}\s", s) or s.startswith("- "):
                break
            para.append(s.strip())
            i += 1
        if para:
            text = " ".join(para)
            out.append(f"<p>{inline_md(html.escape(text))}</p>")
    close_ul()
    close_faq_list()
    if chapter_open:
        out.append("</section>")
    return "\n".join(out)

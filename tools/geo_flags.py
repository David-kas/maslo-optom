# -*- coding: utf-8 -*-
"""Разметка флагов по регионам поставок (assets/flags)."""

GEO_GROUPS = [
    (
        "Россия",
        [("ru.svg", "Россия")],
    ),
    (
        "Ближнее зарубежье",
        [
            ("by.svg", "Беларусь"),
            ("kz.svg", "Казахстан"),
            ("uz.svg", "Узбекистан"),
        ],
    ),
    (
        "Страны ЕС",
        [("eu.svg", "Европейский союз")],
    ),
    (
        "Китай",
        [("cn.svg", "Китай")],
    ),
    (
        "Ближний Восток",
        [
            ("tr.svg", "Турция"),
            ("ae.svg", "ОАЭ"),
            ("sa.svg", "Саудовская Аравия"),
            ("qa.svg", "Катар"),
            ("om.svg", "Оман"),
            ("ir.svg", "Иран"),
            ("eg.svg", "Египет"),
        ],
    ),
    (
        "Африка",
        [
            ("ma.svg", "Марокко"),
            ("dz.svg", "Алжир"),
        ],
    ),
]


def geo_flags_html(prefix: str = "../") -> str:
    flag_path = f"{prefix}assets/flags/"
    blocks = ['<div class="geo-grid" aria-label="Регионы поставок">']
    for title, flags in GEO_GROUPS:
        blocks.append(f'<section class="geo-region"><h3 class="geo-region__title">{title}</h3><div class="market-flags">')
        for fname, alt in flags:
            blocks.append(
                f'<img src="{flag_path}{fname}" width="40" height="28" alt="{alt}" title="{alt}" loading="lazy" decoding="async">'
            )
        blocks.append("</div></section>")
    blocks.append("</div>")
    return "\n".join(blocks)


def geo_flags_compact(prefix: str = "") -> str:
    """Одна строка всех уникальных флагов для превью на главной."""
    seen = set()
    imgs = []
    for _title, flags in GEO_GROUPS:
        for fname, alt in flags:
            if fname in seen:
                continue
            seen.add(fname)
            imgs.append(
                f'<img src="{prefix}assets/flags/{fname}" width="32" height="22" alt="" title="{alt}" loading="lazy" class="market-flags__item">'
            )
    return f'<div class="market-flags market-flags--compact" aria-hidden="true">{"".join(imgs)}</div>'

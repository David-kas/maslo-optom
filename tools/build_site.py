# -*- coding: utf-8 -*-
"""Сборка статического многостраничного сайта."""
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from heading_titles import ID_TITLES  # noqa: E402
from layout import page_shell, callback_form, canonical_url  # noqa: E402
from md_to_html import md_to_html  # noqa: E402
from faq_guide import faq_json_ld_from_guide  # noqa: E402
from page_bodies import inner, faq_json_ld  # noqa: E402
from geo_flags import geo_flags_compact  # noqa: E402
from site_config import PAGES, SITE_ORIGIN  # noqa: E402


def guide_toc_html():
    items = [
        f'<li><a href="#{sid}">{title}</a></li>'
        for sid, title in ID_TITLES.items()
        if sid != "id-oglavlenie"
    ]
    return f"""
<nav class="guide-toc" aria-label="Навигация по справочнику" id="guide-start">
  <p style="margin:0 0 10px;font-weight:700">Разделы</p>
  <ol>{''.join(items)}</ol>
</nav>"""


def home_body():
    md_path = ROOT / "content" / "home_guide.md"
    guide_html = md_to_html(md_path.read_text(encoding="utf-8"))
    top = """
<section class="home-quick" aria-label="Главное о предприятии">
  <div class="home-quick__grid">
    <article class="product-spot product-spot--oil">
      <a class="product-spot__media" href="maslo-podsolnechnoe/">
        <img src="assets/sunflower-oil.jpg" width="1000" height="562" alt="Нерафинированное масло прессового отжима — золотистое, с лёгкой мутностью" loading="lazy" decoding="async">
      </a>
      <div class="product-spot__body">
        <p class="product-spot__tag">ГОСТ 1129-2013 · I сорт</p>
        <h2>Масло оптом</h2>
        <p>Прессовый отжим: бочки 200&nbsp;л, еврокубы, налив в цистерну. Минимальная партия в материалах — бочка; актуальный порог уточняйте.</p>
        <a class="btn-cta" href="maslo-podsolnechnoe/">Условия поставки</a>
      </div>
    </article>
    <article class="product-spot product-spot--cake">
      <a class="product-spot__media" href="zhmyh-podsolnechnyj/">
        <img src="assets/sunflower-cake.jpg" width="1000" height="562" alt="Подсолнечный жмых ракушка и дроблёный — кормовая фактура" loading="lazy" decoding="async">
      </a>
      <div class="product-spot__body">
        <p class="product-spot__tag">ГОСТ 80-96</p>
        <h2>Жмых</h2>
        <p>«Ракушка» или дроблёный — мешки 30&nbsp;кг, биг-бэги, россыпь. Показатель протеина — по документам партии.</p>
        <a class="btn-cta btn-cta--ghost" href="zhmyh-podsolnechnyj/">Характеристики жмыха</a>
      </div>
    </article>
  </div>
  <div class="home-cta-row">
    <a class="btn-cta" href="#zvonok">Заказать звонок</a>
    <a class="btn-cta btn-cta--ghost" href="kontakty/">Контакты и карта</a>
  </div>
</section>
<section class="home-strip">
  <div class="home-strip__copy">
    <h2>Своё поле — своя переработка</h2>
    <p>КФХ Малышева в Прихопёрье (Саратовская область): выращивание подсолнечника, прессовый отжим и отгрузка масла и жмыха. Сырьё — преимущественно с собственных полей.</p>
    <p><a href="proizvodstvo/">Как устроено производство</a> · <a href="upakovka-i-otgruzka/">Тара и отгрузка</a></p>
  </div>
  <figure class="home-strip__media">
    <img src="assets/processing-plant.jpg" width="1200" height="800" alt="Линия прессования на заводе — иллюстрация площадки" loading="lazy" decoding="async">
  </figure>
</section>
<section class="home-steps" aria-labelledby="home-steps-title">
  <div class="section-head section-head--center">
    <h2 id="home-steps-title">Как начать сотрудничество</h2>
    <p>Без лишней бюрократии на первом шаге — дальше условия фиксируем в договоре.</p>
  </div>
  <div class="steps">
    <div class="step"><strong>Запрос</strong><p>Позвоните, напишите или оставьте заявку: объём, продукт, дата.</p></div>
    <div class="step"><strong>КП и тара</strong><p>Согласуем упаковку, документы, логистику и базис.</p></div>
    <div class="step"><strong>Отгрузка</strong><p>Погрузка на площадке по договору, сопроводительные документы на партию.</p></div>
  </div>
</section>
"""
    flags_compact = geo_flags_compact("")
    cards = f"""
<section id="katalog" aria-labelledby="katalog-title">
  <div class="section-head">
    <h2 id="katalog-title">Продукция и услуги</h2>
    <p>Оптовые поставки и переработка — условия согласуются индивидуально.</p>
  </div>
  <div class="cards cards--rich">
    <article class="card card--media"><a class="card__thumb" href="maslo-podsolnechnoe/"><img src="assets/sunflower-oil.jpg" width="480" height="320" alt="" loading="lazy"></a><h3>Масло оптом</h3><p>I сорт, ГОСТ 1129-2013. Бочки, еврокубы, налив.</p><a class="card-link" href="maslo-podsolnechnoe/">Подробнее</a></article>
    <article class="card card--media"><a class="card__thumb" href="zhmyh-podsolnechnyj/"><img src="assets/sunflower-cake.jpg" width="480" height="320" alt="" loading="lazy"></a><h3>Жмых</h3><p>ГОСТ 80-96. Мешки, биг-бэги, россыпь.</p><a class="card-link" href="zhmyh-podsolnechnyj/">Подробнее</a></article>
    <article class="card card--media"><a class="card__thumb" href="zakupka-semyan/"><img src="assets/sunflower-hero.jpg" width="480" height="320" alt="" loading="lazy"></a><h3>Закупка семян</h3><p>Выкуп подсолнечника на переработку.</p><a class="card-link" href="zakupka-semyan/">Условия</a></article>
    <article class="card card--media"><a class="card__thumb" href="davaldcheskaya-pererabotka/"><img src="assets/storage-tanks.jpg" width="480" height="320" alt="" loading="lazy"></a><h3>Давальческая переработка</h3><p>Сырьё заказчика → масло и жмых.</p><a class="card-link" href="davaldcheskaya-pererabotka/">Этапы</a></article>
    <article class="card card--media"><a class="card__thumb" href="upakovka-i-otgruzka/"><img src="assets/packing-bigbags-enhanced.jpg" width="480" height="320" alt="" loading="lazy"></a><h3>Упаковка</h3><p>Тара для масла и жмыха.</p><a class="card-link" href="upakovka-i-otgruzka/">Варианты</a></article>
    <article class="card card--media"><a class="card__thumb" href="kontakty/"><img src="assets/dispatch-area.jpg" width="480" height="320" alt="" loading="lazy"></a><h3>Контакты</h3><p>Телефоны, карта, обратный звонок.</p><a class="card-link" href="kontakty/">Связаться</a></article>
  </div>
</section>
<div class="facts-grid" aria-label="Подтверждённые факты">
  <div class="fact"><strong>С 2007 года</strong>Трудимся во благо людей — заявление компании.</div>
  <div class="fact"><strong>Своё сырьё</strong>Основной объём — подсолнечник Прихопёрья.</div>
  <div class="fact"><strong>Жмых</strong>Протеин 38 %+ — заявленный показатель, уточняйте по документам партии.</div>
  <div class="fact"><strong>Розлив в бутылки</strong>Направление в разработке, не основное предложение.</div>
</div>
<section class="home-audience" aria-labelledby="audience-title">
  <div class="section-head"><h2 id="audience-title">Для кого поставки</h2></div>
  <div class="cards cards--compact">
    <article class="card"><img src="assets/poultry-farm.jpg" width="400" height="260" alt="Птицефабрика — иллюстрация сегмента покупателей" loading="lazy" class="card__inline-img"><h3>Кормовые</h3><p>Комбикормовые заводы, фермы.</p><a class="card-link" href="kormovye-pokupateli/">Подробнее</a></article>
    <article class="card"><img src="assets/bottled-oil-assortment.jpg" width="400" height="260" alt="Планируемая фасовка: бутылки с нерафинированным мутноватым маслом" loading="lazy" class="card__inline-img card__inline-img--oil"><h3>Пищевая переработка</h3><p>Масло I сорта для производств.</p><a class="card-link" href="pishchevaya-pererabotka/">Подробнее</a></article>
    <article class="card card--geo"><h3>География</h3>{flags_compact}<p>Поставки по России, СНГ, ЕС, Китаю, Ближнему Востоку и Африке — условия согласуем по телефону или при встрече с менеджером.</p><a class="card-link" href="geografiya-postavok/">Все направления</a></article>
  </div>
</section>
"""
    guide_block = f"""
<section class="guide-section" aria-labelledby="guide-heading">
  <div class="section-head">
    <h2 id="guide-heading">Справочник для оптовых закупщиков</h2>
  </div>
  <details class="guide-disclosure">
    <summary>Развернуть справочник</summary>
    <div class="guide-layout">
      {guide_toc_html()}
      <div class="long-guide prose--wide">{guide_html}</div>
    </div>
  </details>
  <p class="guide-section__teaser"><a href="voprosy-i-otvety/">Короткий FAQ</a> · <a href="#id-voprosy-i-otvety" data-open-guide>Все вопросы ниже</a> · <a href="#zvonok">Позвонить</a></p>
</section>
"""
    return top + cards + guide_block + callback_form(0)


def write_page(pg):
    slug = pg["slug"]
    depth = pg["depth"]
    if slug == "":
        body = home_body()
        guide_md = (ROOT / "content" / "home_guide.md").read_text(encoding="utf-8")
        home_faq_ld = faq_json_ld_from_guide(guide_md, limit=12)
        extra_home_ld = [home_faq_ld] if home_faq_ld else None
        html_doc = page_shell(
            slug=slug,
            depth=depth,
            title=pg["title"],
            description=pg["description"],
            h1=pg["h1"],
            body_html=body,
            hero=True,
            extra_json_ld=extra_home_ld,
        )
        out = ROOT / "index.html"
    else:
        body = inner(slug, callback_form)
        if slug == "kontakty":
            body += callback_form(depth)
        crumbs = None if slug == "karta-sajta" else [(pg["nav_label"], None)]
        extra_ld = [faq_json_ld()] if slug == "voprosy-i-otvety" else None
        html_doc = page_shell(
            slug=slug,
            depth=depth,
            title=pg["title"],
            description=pg["description"],
            h1=pg["h1"],
            body_html=body,
            breadcrumbs=crumbs,
            extra_json_ld=extra_ld,
            hero=False,
        )
        out = ROOT / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    return out


def write_sitemap():
    today = date.today().isoformat()
    urls = []
    for pg in PAGES:
        if pg["slug"] in ("karta-sajta",):
            continue
        loc = canonical_url(pg["slug"])
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n  </url>")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots():
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_ORIGIN}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_404():
    pg = next(p for p in PAGES if p["slug"] == "")
    body = '<p>Запрашиваемая страница не найдена. Перейдите на <a href="index.html">главную</a> или <a href="karta-sajta/index.html">карту сайта</a>.</p>'
    doc = page_shell(
        slug="404",
        depth=0,
        title="Страница не найдена | КФХ Малышева",
        description="Ошибка 404",
        h1="Страница не найдена",
        body_html=body,
        hero=False,
    )
    (ROOT / "404.html").write_text(doc, encoding="utf-8")


def count_home_words():
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<div class="long-guide[^>]*>(.*?)</div>\s*</div>\s*</section>\s*<section class="callback-panel"', text, re.S)
    if not m:
        m = re.search(r'class="long-guide[^>]*>(.*?)</section>\s*<section class="callback-panel"', text, re.S)
    if not m:
        return 0
    inner_text = re.sub(r"<[^>]+>", " ", m.group(1))
    inner_text = re.sub(r"\s+", " ", inner_text).strip()
    return len(re.findall(r"[\w\u0400-\u04FF]+", inner_text))


def main():
    for pg in PAGES:
        write_page(pg)
    write_sitemap()
    write_robots()
    write_404()
    w = count_home_words()
    print(f"Built {len(PAGES)} pages. Home guide words: {w}")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()

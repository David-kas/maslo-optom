# -*- coding: utf-8 -*-
import html
import json
from site_config import (
    SITE_ORIGIN,
    SITE_NAME,
    LEGAL_NAME,
    INN,
    OGRNIP,
    OKPO,
    MOTTO,
    ADDR_POSTAL,
    PHONE_PRIMARY,
    PHONE_PRIMARY_TEL,
    PHONE_SECONDARY,
    PHONE_SECONDARY_TEL,
    EMAIL,
    MESSENGERS,
    PAGES,
)

THEME_BOOT = """<script>
(function(){
  var k='kfh-malyshev-theme', s=null;
  try{s=localStorage.getItem(k);}catch(e){}
  if(s!=='light'&&s!=='dark'){s=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
  document.documentElement.setAttribute('data-theme',s);
})();
</script>"""


def prefix(depth):
    return "../" * depth if depth else ""


def canonical_url(slug):
    if not slug:
        return SITE_ORIGIN + "/"
    return f"{SITE_ORIGIN}/{slug}/"


def nav_markup(depth, active_slug):
    p = prefix(depth)
    main = [pg for pg in PAGES if not pg.get("footer_only")]
    primary_slugs = {"", "maslo-podsolnechnoe", "zhmyh-podsolnechnyj", "proizvodstvo", "zakupka-semyan", "kontakty"}
    primary = [pg for pg in main if pg["slug"] in primary_slugs]
    more = [pg for pg in main if pg["slug"] not in primary_slugs]

    def link(pg):
        href = p if not pg["slug"] else f"{p}{pg['slug']}/"
        cur = ' aria-current="page"' if pg["slug"] == active_slug else ""
        return f'<li><a href="{href}"{cur}>{html.escape(pg["nav_label"])}</a></li>'

    return f"""
<nav class="site-nav" id="site-nav" aria-label="Основная навигация">
  <ul>
    {''.join(link(pg) for pg in primary)}
    <li class="submenu-wrap">
      <a href="{p}karta-sajta/" aria-haspopup="true" aria-expanded="false" data-nav-submenu-trigger>Все разделы</a>
      <ul class="submenu" role="menu">
        {''.join(link(pg) for pg in more)}
      </ul>
    </li>
  </ul>
</nav>"""


THEME_TOGGLE_ICONS = """<button type="button" class="theme-toggle" data-theme-toggle aria-label="Включить тёмную тему">
        <svg class="theme-toggle__icon theme-toggle__icon--sun" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
        <svg class="theme-toggle__icon theme-toggle__icon--moon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 7 7 0 1 0 20 14.5z"/></svg>
      </button>"""


def header(depth, active_slug):
    p = prefix(depth)
    return f"""<header class="site-header" role="banner">
  <div class="site-header__inner">
    <a class="site-brand" href="{p}">
      <span class="site-brand__mark">
        <span class="site-brand__kfh">КФХ</span>
        <span class="site-brand__name">Малышева</span>
      </span>
    </a>
    {nav_markup(depth, active_slug)}
    <div class="site-header__tools">
      <a class="header-phone" href="tel:{PHONE_PRIMARY_TEL}">{html.escape(PHONE_PRIMARY)}</a>
      <a class="header-phone-icon" href="tel:{PHONE_PRIMARY_TEL}" aria-label="Позвонить {html.escape(PHONE_PRIMARY)}">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
      </a>
      {THEME_TOGGLE_ICONS}
      <a class="btn-cta btn-cta--call" href="{p}#zvonok">Заказать звонок</a>
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Открыть меню"><span class="nav-toggle__bars" aria-hidden="true"></span><span class="nav-toggle__text">Меню</span></button>
    </div>
  </div>
</header>"""


def messengers_html(depth):
    p = prefix(depth)
    parts = []
    for m in MESSENGERS:
        parts.append(
            f'<a href="{html.escape(m["href"])}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="{html.escape(m["aria"])}">'
            f'<img src="{p}{html.escape(m["icon"])}" width="22" height="22" alt="">'
            f'<span>{html.escape(m["name"])}</span></a>'
        )
    return '<div class="messenger-links">' + "".join(parts) + "</div>"


def footer(depth, active_slug):
    p = prefix(depth)
    product_slugs = {"maslo-podsolnechnoe", "zhmyh-podsolnechnyj", "fasovannoe-maslo", "upakovka-i-otgruzka", "kormovye-pokupateli", "pishchevaya-pererabotka"}
    service_slugs = {"proizvodstvo", "zakupka-semyan", "davaldcheskaya-pererabotka", "dostavka-i-logistika", "geografiya-postavok", "kachestvo-i-dokumenty"}
    info_slugs = {"", "voprosy-i-otvety", "kontakty", "karta-sajta", "politika-konfidentsialnosti"}

    def links_for(slugs):
        out = []
        for pg in PAGES:
            if pg["slug"] not in slugs:
                continue
            href = p if not pg["slug"] else f"{p}{pg['slug']}/"
            out.append(f'<li><a href="{href}">{html.escape(pg["nav_label"])}</a></li>')
        return "\n".join(out)

    policy = f"{p}politika-konfidentsialnosti/"
    return f"""<footer class="site-footer" role="contentinfo">
  <div class="footer-inner">
    <div class="footer-grid">
      <div class="footer-about">
        <a class="footer-brand" href="{p}">{html.escape(SITE_NAME)}</a>
        <p class="footer-motto">{html.escape(MOTTO)}</p>
        <p class="footer-entity">{html.escape(LEGAL_NAME)}</p>
        <a class="footer-cta btn-cta" href="{p}#zvonok">Заказать звонок</a>
      </div>
      <div class="footer-links" aria-label="Разделы сайта">
        <div class="footer-links__col">
          <p class="footer-links__title">Продукция</p>
          <ul class="footer-nav">{links_for(product_slugs)}</ul>
        </div>
        <div class="footer-links__col">
          <p class="footer-links__title">Услуги</p>
          <ul class="footer-nav">{links_for(service_slugs)}</ul>
        </div>
        <div class="footer-links__col">
          <p class="footer-links__title">Информация</p>
          <ul class="footer-nav">{links_for(info_slugs)}</ul>
        </div>
      </div>
      <div class="footer-contact">
        <p class="footer-links__title">Связь</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p><a href="tel:{PHONE_PRIMARY_TEL}">{html.escape(PHONE_PRIMARY)}</a></p>
        <p><a href="tel:{PHONE_SECONDARY_TEL}">{html.escape(PHONE_SECONDARY)}</a></p>
        {messengers_html(depth)}
      </div>
    </div>
    <div class="footer-legal">
      <span>ИНН {INN} · ОГРНИП {OGRNIP}</span>
      <span>{html.escape(ADDR_POSTAL)}</span>
      <a href="{policy}">Политика персональных данных</a>
    </div>
  </div>
</footer>"""


PHONE_SVG = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>"""

CALLBACK_SVG = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 15a4 4 0 0 1-4 4H7l-4 4V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"/><path d="M8 10h8M8 14h5"/></svg>"""


def fab(depth: int = 0):
    p = prefix(depth)
    return f"""<nav class="mobile-dock" aria-label="Звонок и заявка">
  <a class="mobile-dock__action mobile-dock__action--phone" href="tel:{PHONE_PRIMARY_TEL}">
    {PHONE_SVG}
    <span>Позвонить</span>
  </a>
  <a class="mobile-dock__action mobile-dock__action--callback" href="{p}#zvonok">
    {CALLBACK_SVG}
    <span>Заявка</span>
  </a>
</nav>
<button type="button" class="back-top" aria-label="Наверх" title="Наверх">↑</button>"""


def callback_form(depth):
    p = prefix(depth)
    policy = f"{p}politika-konfidentsialnosti/"
    action = "/api/callback"
    return f"""
<section class="callback-panel" id="zvonok" data-callback-form aria-labelledby="callback-title">
  <h2 id="callback-title">Заказать обратный звонок</h2>
  <p class="callback-panel__lead">Оставьте имя и номер — менеджер свяжется с вами.</p>
  <form action="{html.escape(action)}" method="post" novalidate>
    <div class="form-hp" aria-hidden="true">
      <label>Сайт <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
    </div>
    <div class="callback-grid">
      <label>Ваше имя <input name="name" type="text" autocomplete="name" required></label>
      <label>Номер телефона
        <input name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 (___) ___-__-__" required>
      </label>
    </div>
    <label class="consent-row">
      <input name="consent" type="checkbox" value="1" required>
      <span>Согласен на обработку персональных данных по <a href="{policy}">политике</a></span>
    </label>
    <button type="submit" class="btn-cta">Жду звонка</button>
    <p class="form-status" data-form-status hidden role="status"></p>
  </form>
</section>"""


def json_ld_organization():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE_NAME,
        "legalName": LEGAL_NAME,
        "url": SITE_ORIGIN + "/",
        "email": EMAIL,
        "telephone": [PHONE_PRIMARY_TEL, PHONE_SECONDARY_TEL],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "ул. Молодёжная, д. 15",
            "addressLocality": "село Сухая Елань",
            "addressRegion": "Саратовская область",
            "postalCode": "412339",
            "addressCountry": "RU",
        },
    }


def json_ld_website():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "url": SITE_ORIGIN + "/",
        "inLanguage": "ru",
    }


def json_ld_breadcrumbs(slug, crumbs_labels):
    if not crumbs_labels:
        return None
    items = [{"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE_ORIGIN + "/"}]
    pos = 2
    for label, path in crumbs_labels:
        items.append({"@type": "ListItem", "position": pos, "name": label, "item": SITE_ORIGIN + path})
        pos += 1
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def page_shell(
    *,
    slug,
    depth,
    title,
    description,
    h1,
    body_html,
    breadcrumbs=None,
    extra_json_ld=None,
    hero=False,
):
    p = prefix(depth)
    canon = canonical_url(slug if slug != "404" else "")
    og_image = SITE_ORIGIN + "/assets/sunflower-hero.jpg"

    crumb_html = ""
    crumb_ld = []
    if breadcrumbs and slug != "":
        parts = [f'<a href="{p}">Главная</a>']
        for label, href in breadcrumbs:
            if href:
                parts.append(f'<a href="{href}">{html.escape(label)}</a>')
                path = href.replace("../", "/").replace("./", "/")
                if not path.startswith("/"):
                    path = "/" + path
                crumb_ld.append((label, path))
            else:
                parts.append(f'<span aria-current="page">{html.escape(label)}</span>')
                crumb_ld.append((label, canonical_url(slug)))
        crumb_html = f'<nav class="breadcrumbs" aria-label="Хлебные крошки">{" / ".join(parts)}</nav>'

    ld = [json_ld_organization(), json_ld_website()]
    bl = json_ld_breadcrumbs(slug, crumb_ld)
    if bl:
        ld.append(bl)
    if extra_json_ld:
        ld.extend(extra_json_ld)
    ld_script = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"

    if hero:
        main = f"""<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__grid">
    <div class="hero__copy">
      <h1 id="hero-title">{html.escape(h1)}</h1>
      <p class="hero__lead">{html.escape(MOTTO)}</p>
      <p>Нерафинированное масло I сорта и подсолнечный жмых оптом. Прихопёрье, Саратовская область.</p>
      <div class="hero__actions">
        <a class="btn-cta" href="#katalog">Продукция и услуги</a>
        <a class="btn-cta btn-cta--ghost" href="#guide-start">Справочник</a>
      </div>
    </div>
    <aside class="hero__facts" aria-label="Ключевые факты">
      <dl>
        <div><dt>Продукция</dt><dd>Масло ГОСТ 1129-2013 · жмых ГОСТ 80-96</dd></div>
        <div><dt>Опт</dt><dd>Бочки 200 л · еврокубы · налив · мешки и биг-бэги</dd></div>
        <div><dt>Связь</dt><dd><a href="tel:{PHONE_PRIMARY_TEL}" style="color:inherit">{html.escape(PHONE_PRIMARY)}</a></dd></div>
      </dl>
    </aside>
  </div>
</section>
<div class="page-shell prose--wide">
{body_html}
</div>
</main>"""
    else:
        main = f"""<main id="main">
<div class="page-shell">
  <div class="page-title-block">
    <h1>{html.escape(h1)}</h1>
    {crumb_html}
  </div>
  {body_html}
</div>
</main>"""

    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{html.escape(canon or SITE_ORIGIN + '/')}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{html.escape(canon or SITE_ORIGIN + '/')}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
{THEME_BOOT}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&amp;family=Golos+Text:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="{p}css/site.css">
{ld_script}
</head>
<body>
<a class="skip-link" href="#main">К основному содержанию</a>
{header(depth, slug)}
{main}
{footer(depth, slug)}
{fab(depth)}
<script src="{p}js/site.js" defer></script>
<script src="{p}js/form.js" defer></script>
</body>
</html>"""

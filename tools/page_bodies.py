# -*- coding: utf-8 -*-
"""HTML-тела внутренних страниц (краткие уникальные тексты)."""

from geo_flags import geo_flags_html
from site_config import FACTORY_LAT, FACTORY_LON, osm_map_embed_src


def cta_end():
    return """
<div class="cta-band">
  <div>
    <h2>Обсудим объём и условия</h2>
    <p style="margin:8px 0 0">Позвоните или закажите обратный звонок — без обязательств.</p>
  </div>
  <a class="btn-cta" href="../kontakty/#zvonok">Заказать звонок</a>
</div>"""


def inner(slug: str, form) -> str:
    """form — callback_form для страницы контактов."""
    pages = {
        "maslo-podsolnechnoe": maslo,
        "zhmyh-podsolnechnyj": zhmyh,
        "fasovannoe-maslo": fasovka,
        "proizvodstvo": proizvodstvo,
        "zakupka-semyan": zakupka,
        "davaldcheskaya-pererabotka": davald,
        "upakovka-i-otgruzka": upakovka,
        "dostavka-i-logistika": dostavka,
        "kormovye-pokupateli": kormovye,
        "pishchevaya-pererabotka": pishchevaya,
        "geografiya-postavok": geografia,
        "kachestvo-i-dokumenty": kachestvo,
        "voprosy-i-otvety": faq,
        "kontakty": kontakty,
        "politika-konfidentsialnosti": politika,
        "karta-sajta": karta,
    }
    return pages[slug](form)


def maslo(form):
    return f"""
<div class="split">
  <div class="split__body">
    <p>Нерафинированное подсолнечное масло <strong>прессового отжима, I сорт</strong> по <strong>ГОСТ 1129-2013</strong> (ТН ВЭД <strong>1512.11</strong>). Назначение по стандарту включает употребление в пищу, производство пищевых продуктов и промышленную переработку; применение в кормлении — как энергетический компонент комбикормов.</p>
  </div>
  <figure class="split__media"><img src="../assets/sunflower-oil.jpg" width="1000" height="562" alt="Нерафинированное масло прессового отжима в банке — слегка мутное" loading="lazy"></figure>
</div>
<h2>Отгрузка</h2>
<p>Подтверждённые варианты: бочки <strong>200 л</strong>, еврокубы <strong>1000 л</strong>, налив в автоцистерны на заводе. Организацию доставки обсуждаем индивидуально — сроки, базис и стоимость не фиксируются на сайте.</p>
<p>Минимальная партия в исходных материалах указана как бочка 200 л; актуальный порог для вашей отгрузки уточняйте у менеджера.</p>
<h2>Вопросы покупателя</h2>
<ul>
<li>требуемая дата и объём партии;</li>
<li>тип тары и возможность наливa;</li>
<li>перечень сопроводительных документов;</li>
<li>условия оплаты и базис поставки.</li>
</ul>
<p><a href="../upakovka-i-otgruzka/">Упаковка и отгрузка</a> · <a href="../kachestvo-i-dokumenty/">Качество и документы</a> · <a href="../dostavka-i-logistika/">Доставка</a></p>
{cta_end()}
"""


def zhmyh(form):
    return f"""
<p>Подсолнечный жмых по <strong>ГОСТ 80-96</strong> (код <strong>2306.30</strong>) в формах <strong>«ракушка»</strong> или <strong>«дроблёный»</strong>. Назначение по стандарту — прямое введение в рацион животных и производство комбинированной продукции.</p>
<div class="note-neutral"><strong>Заявленный показатель протеина:</strong> в исходных материалах указано «38&nbsp;%+ сырой протеин на сухое вещество, не менее». Это не гарантия для каждой партии без подтверждения протоколом анализа — запрашивайте документы на конкретную отгрузку.</div>
<figure><img src="../assets/sunflower-cake.jpg" width="1000" height="562" alt="Подсолнечный жмых ракушка на деревянном поддоне" loading="lazy"></figure>
<p class="note-plan">Планируем выпуск <strong>гранулированного жмыха</strong> и гранулированной подсолнечной лузги. Статус направления уточняйте у менеджера.</p>
<h2>Отгрузка</h2>
<p>Мешки по <strong>30 кг</strong>, биг-бэги по <strong>1000 кг</strong>, россыпью в зерновозах. Другие варианты тары — по запросу покупателя.</p>
<p><a href="../kormovye-pokupateli/">Для кормовых покупателей</a> · <a href="../upakovka-i-otgruzka/">Упаковка</a></p>
{cta_end()}
"""


def fasovka(form):
    return f"""
<figure><img src="../assets/bottled-oil-assortment.jpg" width="1536" height="1024" alt="Бутылки 0,5–5 л с нерафинированным слегка мутным маслом — планируемая линейка" loading="lazy" class="card__inline-img--oil"></figure>
<p class="note-plan"><strong>Планируемый розлив</strong> в потребительскую тару. В исходнике перечислены форматы <strong>0,5 л, 1 л, 1,5 л и 5 л</strong> (бутылки 5 л — с крышкой и ручкой). Не считайте фасовку обязательно доступной сейчас: условия и сроки согласуются по запросу.</p>
<p>Основной текущий фокус предприятия — оптовые поставки масла в промышленной таре. Подробнее: <a href="../maslo-podsolnechnoe/">масло оптом</a>.</p>
{cta_end()}
"""


def proizvodstvo(form):
    return f"""
<p>Большая часть сырья, которое перерабатывается на заводе, — собственный подсолнечник, выращенный в Прихопёрье. Ниже — фотографии производства с пояснениями; они иллюстрируют типовые процессы и площадку, а не отдельный договор с изображёнными объектами.</p>
<div class="site-gallery">
<figure><img src="../assets/processing-plant.jpg" alt="Оборудование линии прессования подсолнечного масла" loading="lazy"><figcaption>Производственный цех · иллюстрация</figcaption></figure>
<figure><img src="../assets/storage-tanks.jpg" alt="Резервуары для хранения масла" loading="lazy"><figcaption>Склад и резервуары · иллюстрация</figcaption></figure>
<figure><img src="../assets/dispatch-area.jpg" alt="Площадка отгрузки, автоцистерна" loading="lazy"><figcaption>Зона отгрузки · иллюстрация</figcaption></figure>
<figure><img src="../assets/sunflower-hero.jpg" alt="Поле подсолнечника в Прихопёрье" loading="lazy"><figcaption>Поля хозяйства</figcaption></figure>
</div>
<p><a href="../zakupka-semyan/">Закупка семян</a> · <a href="../davaldcheskaya-pererabotka/">Давальческая переработка</a></p>
{cta_end()}
"""


def zakupka(form):
    return f"""
<p>Закупаем подсолнечник для переработки на условиях, согласованных с продавцом. По договорённости можем забрать сырьё от ворот поставщика своим транспортом.</p>
<h2>Что указать в предложении</h2>
<ul>
<li>объём партии и ориентировочную дату готовности;</li>
<li>адрес погрузки и контакт на месте;</li>
<li>качество и влажность (если известны);</li>
<li>желаемые условия оплаты и вывоза.</li>
</ul>
<p><a href="../davaldcheskaya-pererabotka/">Если нужна переработка вашего сырья</a> — см. давальческий раздел.</p>
<div class="steps" aria-label="Этапы закупки">
  <div class="step"><strong>Заявка</strong><p>Объём, адрес погрузки, контакт.</p></div>
  <div class="step"><strong>Согласование</strong><p>Цена и дата вывоза с продавцом.</p></div>
  <div class="step"><strong>Вывоз</strong><p>По договорённости — ваш или наш транспорт.</p></div>
</div>
{cta_end()}
"""


def davald(form):
    return f"""
<p>Основной объём завод перерабатывает из собственного подсолнечника. Дополнительно возможна <strong>давальческая переработка</strong>: вы передаёте семена, мы производим масло и жмых, условия фиксируются в договоре.</p>
<div class="steps" aria-label="Этапы давальческой переработки">
  <div class="step"><strong>Сырьё</strong><p>Привозите сами или забираем у вас (по согласованию).</p></div>
  <div class="step"><strong>Переработка</strong><p>Масло и жмых на заводе КФХ Малышева.</p></div>
  <div class="step"><strong>Расчёт</strong><p>Оплата услуги или частично готовой продукцией по договору.</p></div>
</div>
<p>Стоимость, минимальный объём и география забора сырья — <strong>по согласованию</strong>.</p>
{cta_end()}
"""


def upakovka(form):
    return f"""
<table class="data-table">
  <caption class="sr-only">Сводка по таре</caption>
  <thead><tr><th>Продукт</th><th>Варианты отгрузки</th></tr></thead>
  <tbody>
    <tr><td>Масло</td><td>Бочки 200 л · еврокубы 1000 л · налив в автоцистерны на заводе</td></tr>
    <tr><td>Жмых</td><td>Мешки 30 кг · биг-бэги 1000 кг · россыпь в зерновозах</td></tr>
  </tbody>
</table>
<div class="site-gallery">
<figure><img src="../assets/packing-ibc-enhanced.jpg" alt="Еврокубы для наливa подсолнечного масла" loading="lazy"><figcaption>Масло в еврокубах · иллюстрация</figcaption></figure>
<figure><img src="../assets/packing-bigbags-enhanced.jpg" alt="Жмых в биг-бэгах" loading="lazy"><figcaption>Жмых в биг-бэгах</figcaption></figure>
<figure><img src="../assets/packing-bulk-enhanced.jpg" alt="Насыпная отгрузка жмыха" loading="lazy"><figcaption>Жмых россыпью</figcaption></figure>
</div>
{cta_end()}
"""


def dostavka(form):
    return f"""
<p>Доставку и базис поставки согласовываем индивидуально. В исходных материалах упомянуты автомобильный, железнодорожный и морской транспорт — конкретная схема зависит от объёма, направления и тары.</p>
<h2>Данные для расчёта</h2>
<ul>
<li>продукт (масло / жмых);</li>
<li>объём и тип тары;</li>
<li>пункт назначения и желаемые сроки;</li>
<li>требования к документам и разгрузке.</li>
</ul>
<p>См. также <a href="../geografiya-postavok/">географию поставок</a> — куда отгружаем и как согласовать условия.</p>
{cta_end()}
"""


def kormovye(form):
    return f"""
<p>Жмых подсолнечника применяют в рационах КРС, свиней, птицы и в рецептурах комбикормов как источник протеина и энергии. Мы не обещаем конкретных кормовых эффектов без спецификации вашего технолога — согласуйте вводимость с нормами и анализом партии.</p>
<div class="site-gallery">
<figure><img src="../assets/cattle.jpg" alt="Иллюстрация: животноводческий комплекс" loading="lazy"><figcaption>Животноводство · иллюстрация применения</figcaption></figure>
<figure><img src="../assets/poultry-farm.jpg" alt="Иллюстрация: птицефабрика" loading="lazy"><figcaption>Птицеводство</figcaption></figure>
<figure><img src="../assets/hens.jpg" alt="Иллюстрация: кормление птицы" loading="lazy"><figcaption>Корма для птицы</figcaption></figure>
<figure><img src="../assets/fish-farm.jpg" alt="Иллюстрация: рыбное хозяйство" loading="lazy"><figcaption>Рыбные хозяйства</figcaption></figure>
</div>
<p><a href="../zhmyh-podsolnechnyj/">Жмых оптом</a></p>
{cta_end()}
"""


def pishchevaya(form):
    return f"""
<p>Масло I сорта прессового отжима по ГОСТ 1129-2013 предназначено, в том числе, для пищевых производств. Пригодность к конкретному процессу (фритюр, майонез, выпечка, дальнейшая рафинация) зависит от вашей спецификации — запрашивайте параметры и документы на партию.</p>
<p class="note-plan">Рафинация и дезодорация в исходнике указаны как <strong>план развития</strong>, а не обязательно доступная услуга сейчас.</p>
<p><a href="../maslo-podsolnechnoe/">Масло оптом</a> · <a href="../kachestvo-i-dokumenty/">Документы</a></p>
{cta_end()}
"""


def geografia(form):
    flags = geo_flags_html("../")
    return f"""
<p class="lead">Поставляем подсолнечное масло и жмых оптом по <strong>России</strong>, в страны <strong>ближнего зарубежья</strong>, <strong>ЕС</strong>, <strong>Китай</strong>, на <strong>Ближний Восток</strong> и в <strong>Африку</strong>. Конкретные маршруты, документы, базис и сроки согласуем индивидуально.</p>
<p>Чтобы собрать коммерческое предложение под вашу страну: позвоните, напишите на почту или оставьте заявку на обратный звонок — на встрече с менеджером можно сразу обсудить объём, тару и логистику.</p>
{flags}
<p>Транспорт — автомобильный, при необходимости железнодорожный и морской. Для расчёта укажите продукт, объём, пункт назначения и желаемые даты.</p>
<p><a href="../dostavka-i-logistika/">Доставка и логистика</a> · <a href="../kontakty/#zvonok">Связаться с менеджером</a></p>
{cta_end()}
"""


def kachestvo(form):
    return f"""
<h2>Стандарты продукции</h2>
<ul>
<li>Масло: ГОСТ 1129-2013, HS 1512.11, I сорт, прессовый отжим.</li>
<li>Жмых: ГОСТ 80-96, HS 2306.30.</li>
</ul>
<p>На партию по запросу могут предоставляться декларация о соответствии, протокол испытаний и иные документы — <strong>фактический перечень уточняйте</strong> для конкретной отгрузки, не ожидайте фиксированного набора на сайте.</p>
<p>Показатель протеина в жмыхе: см. формулировку на странице <a href="../zhmyh-podsolnechnyj/">жмыха</a>.</p>
{cta_end()}
"""


def faq(form):
    faq_items = [
        (
            "С какой партии можно заказать масло?",
            "Обычно стартуем с бочки 200 л; для крупных объёмов — еврокуб 1000 л или налив в вашу цистерну. Назовите нужный объём — подберём тару и срок.",
        ),
        (
            "Как быстро связаться и получить цену?",
            "Позвоните по номеру в шапке, напишите на почту или оставьте заявку на обратный звонок — имя и телефон достаточно для первого разговора.",
        ),
        (
            "Есть ли розлив в бутылки 0,5–5 л?",
            "Направление в разработке; основной фокус сейчас — опт в бочках, кубах и наливе. Актуальность фасовки уточним при заявке.",
        ),
        (
            "Можно ли привезти свой подсолнечник на переработку?",
            "Да, работаем по давальческой схеме: ваше семя — наше масло и жмых, условия в договоре. Подробнее — в разделе давальческой переработки.",
        ),
        (
            "Отгружаете ли за пределы Саратовской области?",
            "Да, по России и за рубеж — Россия, СНГ, ЕС, Китай, Ближний Восток, Африка. Условия и документы на партию согласуем по телефону или на встрече с менеджером.",
        ),
    ]
    acc = "\n".join(
        f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq_items
    )
    return f"""<div class="faq-list">{acc}</div>{cta_end()}"""


def faq_json_ld():
    import json

    items = [
        (
            "С какой партии можно заказать масло?",
            "Обычно стартуем с бочки 200 л; для крупных объёмов — еврокуб 1000 л или налив в цистерну.",
        ),
        (
            "Как быстро связаться и получить цену?",
            "Позвоните, напишите на почту или оставьте заявку на обратный звонок на сайте.",
        ),
        (
            "Есть ли розлив в бутылки 0,5–5 л?",
            "Направление в разработке; основной фокус — опт в бочках, кубах и наливе.",
        ),
        (
            "Можно ли привезти свой подсолнечник на переработку?",
            "Да, по давальческой схеме — условия в договоре.",
        ),
        (
            "Отгружаете ли за пределы Саратовской области?",
            "Да, по России и за рубеж. Условия согласуем с менеджером.",
        ),
    ]
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in items
        ],
    }


def kontakty(form):
    return f"""
<div class="split split--reverse">
  <div class="split__body">
    <p><strong>Адрес хозяйства (почтовый):</strong> 412339, Саратовская область, Балашовский район, село Сухая Елань, улица Молодёжная, дом 15.</p>
    <p><strong>Точка завода (координаты):</strong> {FACTORY_LAT}, {FACTORY_LON} — не смешивайте с почтовым адресом хозяйства.</p>
    <p>
      <a href="https://yandex.ru/maps/?rtext=~{FACTORY_LAT}%2C{FACTORY_LON}&amp;rtt=auto" target="_blank" rel="noopener noreferrer">Маршрут в Яндекс Картах</a>
      ·
      <a href="https://www.openstreetmap.org/?mlat={FACTORY_LAT}&amp;mlon={FACTORY_LON}#map=16/{FACTORY_LAT}/{FACTORY_LON}" target="_blank" rel="noopener noreferrer">Открыть на OpenStreetMap</a>
    </p>
    <p>Email: <a href="mailto:denmsr90@yandex.ru">denmsr90@yandex.ru</a><br>
    <a href="tel:+79093398167">+7 (909) 339-81-67</a> · <a href="tel:+79603543555">+7 (960) 354-35-55</a></p>
  </div>
  <div class="split__media contact-map">
    <iframe title="Карта — точка завода (OpenStreetMap)" src="{osm_map_embed_src()}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    <p class="contact-map__credit"><a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">© OpenStreetMap</a></p>
  </div>
</div>
"""


def politika(form):
    return f"""
<p class="note-neutral"><strong>Черновик.</strong> Перед публикацией оператор персональных данных должен подтвердить реквизиты, цели обработки, сроки хранения, права субъектов и адрес для обращений.</p>
<p>Оператор (по данным сайта): ИП Глава КФХ Малышев Сергей Валентинович, ИНН 644005411691.</p>
<p>Форма обратного звонка передаёт только имя и телефон на сервер сайта; доставка заявки владельцу настраивается через переменные окружения (см. <code>.env.example</code>).</p>
<p>[МЕСТО ДЛЯ: полный текст политики, реквизиты для обращений, cookies, если используются]</p>
"""


def karta(form):
    from site_config import PAGES

    links = []
    for pg in PAGES:
        if pg.get("footer_only") and pg["slug"] == "karta-sajta":
            continue
        href = "../" if not pg["slug"] else f"../{pg['slug']}/"
        links.append(f'<li><a href="{href}">{pg["nav_label"]}</a> — {pg["description"][:80]}…</li>')
    return "<ul>" + "\n".join(links) + "</ul>"

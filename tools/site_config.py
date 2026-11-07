# -*- coding: utf-8 -*-
"""Константы сайта — единый источник фактов для сборки."""

SITE_ORIGIN = "https://xn--64-6kc2ateqay6b.xn--p1ai"
SITE_NAME = "КФХ Малышева"
LEGAL_NAME = "ИП Глава КФХ Малышев Сергей Валентинович"
INN = "644005411691"
OGRNIP = "307644006600182"
OKPO = "0151587065"
MOTTO = "Трудимся во благо людей с 2007 года"

ADDR_POSTAL = (
    "412339, Саратовская область, Балашовский район, "
    "село Сухая Елань, улица Молодёжная, дом 15"
)
FACTORY_LAT = 51.244890
FACTORY_LON = 42.956232


def osm_map_embed_src(*, pad_lon: float = 0.018, pad_lat: float = 0.012) -> str:
    """Встраиваемая карта OpenStreetMap (без рекламных блоков Яндекса)."""
    west = FACTORY_LON - pad_lon
    south = FACTORY_LAT - pad_lat
    east = FACTORY_LON + pad_lon
    north = FACTORY_LAT + pad_lat
    bbox = f"{west}%2C{south}%2C{east}%2C{north}"
    marker = f"{FACTORY_LAT}%2C{FACTORY_LON}"
    return (
        "https://www.openstreetmap.org/export/embed.html"
        f"?bbox={bbox}&layer=mapnik&marker={marker}"
    )

PHONE_PRIMARY = "+7 (909) 339-81-67"
PHONE_PRIMARY_TEL = "+79093398167"
PHONE_SECONDARY = "+7 (960) 354-35-55"
PHONE_SECONDARY_TEL = "+79603543555"
EMAIL = "denmsr90@yandex.ru"

MESSENGERS = [
    {
        "name": "WhatsApp",
        "href": "https://wa.me/79093398167",
        "icon": "assets/whatsapp.svg",
        "aria": "Написать в WhatsApp на номер +7 909 339-81-67",
    },
    {
        "name": "Telegram",
        "href": "https://t.me/+79093398167",
        "icon": "assets/telegram.svg",
        "aria": "Написать в Telegram на номер +7 909 339-81-67",
    },
    {
        "name": "MAX",
        "href": "https://max.ru/u/f9LHodD0cOKcNrY5hsnVmsBNcutdRaI0N8YIgD9gH9MXY-BOVP30ESAWs7U",
        "icon": "assets/max.svg",
        "aria": "Написать в MAX",
    },
]

PAGES = [
    {"slug": "", "path": "index.html", "depth": 0,
     "title": "Масло и жмых подсолнечника оптом | КФХ Малышева, Саратовская область",
     "description": "Нерафинированное подсолнечное масло прессового отжима и жмых оптом от КФХ Малышева. Выращивание и переработка в Прихопёрье. Закупка семян, давальческая переработка. Запросите условия.",
     "h1": "Масло подсолнечное нерафинированное прессового отжима и жмых оптом",
     "nav_label": "Главная"},
    {"slug": "maslo-podsolnechnoe", "path": "maslo-podsolnechnoe/index.html", "depth": 1,
     "title": "Масло подсолнечное нерафинированное оптом | I сорт, прессовый отжим",
     "description": "Оптовая поставка нерафинированного подсолнечного масла I сорта по ГОСТ 1129-2013. Бочки 200 л, еврокубы, налив. КФХ Малышева.",
     "h1": "Масло подсолнечное нерафинированное прессового отжима, I сорт",
     "nav_label": "Масло оптом"},
    {"slug": "zhmyh-podsolnechnyj", "path": "zhmyh-podsolnechnyj/index.html", "depth": 1,
     "title": "Жмых подсолнечный оптом | ракушка, дроблёный, ГОСТ 80-96",
     "description": "Подсолнечный жмых для комбикормов и животноводства. Мешки, биг-бэги, россыпь. Характеристики и документы — по запросу.",
     "h1": "Подсолнечный жмых: ракушка и дроблёный",
     "nav_label": "Жмых"},
    {"slug": "fasovannoe-maslo", "path": "fasovannoe-maslo/index.html", "depth": 1,
     "title": "Фасованное масло в потребительской таре | планируемый розлив",
     "description": "Форматы 0,5–5 л: розлив в потребительскую тару — направление в разработке. Уточняйте актуальный статус у менеджера.",
     "h1": "Масло в потребительской таре",
     "nav_label": "Фасовка"},
    {"slug": "proizvodstvo", "path": "proizvodstvo/index.html", "depth": 1,
     "title": "Производство | выращивание и переработка подсолнечника",
     "description": "КФХ Малышева: поля в Прихопёрье, завод, хранение и отгрузка. Фото производства с пояснениями.",
     "h1": "Выращивание подсолнечника и переработка",
     "nav_label": "Производство"},
    {"slug": "zakupka-semyan", "path": "zakupka-semyan/index.html", "depth": 1,
     "title": "Закупка семян подсолнечника у сельхозпроизводителей",
     "description": "Закупаем подсолнечник на переработку. Как согласовать вывоз, объём и условия.",
     "h1": "Закупка семян подсолнечника",
     "nav_label": "Закупка семян"},
    {"slug": "davaldcheskaya-pererabotka", "path": "davaldcheskaya-pererabotka/index.html", "depth": 1,
     "title": "Давальческая переработка подсолнечника",
     "description": "Переработка сырья заказчика на масло и жмых по договору. Этапы и варианты расчёта.",
     "h1": "Давальческая переработка вашего подсолнечника",
     "nav_label": "Давальческая переработка"},
    {"slug": "upakovka-i-otgruzka", "path": "upakovka-i-otgruzka/index.html", "depth": 1,
     "title": "Упаковка и отгрузка масла и жмыха",
     "description": "Тара и способы отгрузки для масла и жмыха: бочки, еврокубы, налив, мешки, биг-бэги.",
     "h1": "Тара и отгрузка продукции",
     "nav_label": "Упаковка"},
    {"slug": "dostavka-i-logistika", "path": "dostavka-i-logistika/index.html", "depth": 1,
     "title": "Доставка и логистика",
     "description": "Доставка и базис поставки согласуются индивидуально. Какие данные нужны для расчёта.",
     "h1": "Доставка и логистические условия",
     "nav_label": "Доставка"},
    {"slug": "kormovye-pokupateli", "path": "kormovye-pokupateli/index.html", "depth": 1,
     "title": "Жмых для комбикормов и животноводства",
     "description": "Сценарии использования подсолнечного жмыха для ККП, МТФ и птицеводства без неподтверждённых обещаний.",
     "h1": "Для комбикормовых предприятий и животноводства",
     "nav_label": "Кормовые покупатели"},
    {"slug": "pishchevaya-pererabotka", "path": "pishchevaya-pererabotka/index.html", "depth": 1,
     "title": "Масло для пищевых производств",
     "description": "Нерафинированное масло прессового отжима для пищевой промышленности. Документы и спецификации по запросу.",
     "h1": "Для пищевых производств и переработчиков масла",
     "nav_label": "Пищевая переработка"},
    {"slug": "geografiya-postavok", "path": "geografiya-postavok/index.html", "depth": 1,
     "title": "География поставок и экспортные запросы",
     "description": "Поставки масла и жмыха: Россия, ближнее зарубежье, ЕС, Китай, Ближний Восток, Африка. Условия по договорённости с менеджером.",
     "h1": "География поставок",
     "nav_label": "География"},
    {"slug": "kachestvo-i-dokumenty", "path": "kachestvo-i-dokumenty/index.html", "depth": 1,
     "title": "Качество, стандарты и документы на партию",
     "description": "ГОСТ 1129-2013 и ГОСТ 80-96. Какие сопроводительные документы запрашивать у менеджера.",
     "h1": "Качество, стандарты и документы",
     "nav_label": "Качество"},
    {"slug": "voprosy-i-otvety", "path": "voprosy-i-otvety/index.html", "depth": 1,
     "title": "Вопросы и ответы о масле и жмыхе оптом",
     "description": "FAQ: минимальная партия, тара, заявка, доставка, давальческая переработка.",
     "h1": "Частые вопросы",
     "nav_label": "Вопросы и ответы"},
    {"slug": "kontakty", "path": "kontakty/index.html", "depth": 1,
     "title": "Контакты КФХ Малышева | адрес, телефон, карта завода",
     "description": "Телефоны, email, мессенджеры, почтовый адрес хозяйства и координаты точки завода.",
     "h1": "Контакты",
     "nav_label": "Контакты"},
    {"slug": "politika-konfidentsialnosti", "path": "politika-konfidentsialnosti/index.html", "depth": 1,
     "title": "Политика конфиденциальности",
     "description": "Обработка персональных данных на сайте КФХ Малышева. Черновик — требуется подтверждение оператором.",
     "h1": "Политика конфиденциальности",
     "nav_label": "Политика ПДн",
     "footer_only": True},
    {"slug": "karta-sajta", "path": "karta-sajta/index.html", "depth": 1,
     "title": "Карта сайта",
     "description": "Все разделы сайта КФХ Малышева.",
     "h1": "Карта сайта",
     "nav_label": "Карта сайта",
     "footer_only": True},
]

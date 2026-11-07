# -*- coding: utf-8 -*-
"""Человекочитаемые заголовки для id-разделов справочника главной."""

ID_TITLES = {
    "id-oglavlenie": "Оглавление справочника",
    "id-o-predpriyatii": "О предприятии и реквизитах",
    "id-adres-i-koordinaty": "Адрес хозяйства и координаты завода",
    "id-vyrashchivanie-podsolnechnika": "Выращивание подсолнечника",
    "id-pressovyy-otzhim": "Прессовый отжим",
    "id-kontekst-kormovogo-zhmyha": "Жмых в кормовом контексте",
    "id-maslo-dlya-pishchevyh-proizvodstv": "Масло для пищевых производств",
    "id-cheklist-dogovora": "Чек-лист условий договора",
    "id-vhodnoy-kontrol-pokupatelya": "Входной контроль покупателя",
    "id-hranenie-i-sklad": "Хранение и склад",
    "id-logistika-povolzhya": "Логистика в Поволжье",
    "id-davaldcheskie-stsenarii": "Сценарии давальческой переработки",
    "id-zakupka-semjan-dlya-fermerov": "Закупка семян у сельхозпроизводителей",
    "id-eksportnye-peregovory": "Экспортные переговоры",
    "id-planirovanie-vnutri-kholdinga": "Планирование внутри холдинга",
    "id-ustoichivost-i-proishozhdenie": "Происхождение сырья и прослеживаемость",
    "id-maslo-harakteristiki": "Характеристики нерафинированного масла",
    "id-zhmyh-harakteristiki": "Характеристики подсолнечного жмыха",
    "id-upakovka-masla": "Упаковка и отгрузка масла",
    "id-upakovka-zhmyha": "Упаковка и отгрузка жмыха",
    "id-logistika": "Доставка и логистика",
    "id-zakupka-semyan": "Закупка семян подсолнечника",
    "id-davalcheskaya-pererabotka": "Давальческая переработка",
    "id-kachestvo-i-dokumenty": "Качество и документы на партию",
    "id-auditorii-pokupateley": "Кому подходит продукция",
    "id-geografiya-postavok": "География поставок",
    "id-plany-razvitiya": "Планы развития производства",
    "id-sopostavlenie-s-ekstraktsiey": "Прессовый отжим и экстракция",
    "id-kommunikatsiya-s-menedzherom": "Коммуникация с менеджером",
    "id-riski-i-ogranicheniya": "Риски и ограничения",
    "id-primer-pisem-zaprosa": "Примеры письма с запросом",
    "id-etapy-sdelki": "Этапы сделки",
    "id-rol-tehnologa-kkp": "Роль технолога комбикормового завода",
    "id-rol-snabzheniya": "Роль отдела снабжения",
    "id-vzaimodeystvie-s-vet-sluzhboy": "Взаимодействие с ветслужбой",
    "id-dopolnitelnyy-kontekst": "Дополнительный контекст",
    "id-voprosy-i-otvety": "Частые вопросы",
    "id-glossariy": "Глоссарий",
    "id-kak-zaprosit-predlozhenie": "Как запросить коммерческое предложение",
}


def title_for_slug(slug: str, raw: str) -> str:
    key = slug.lower().strip()
    if key in ID_TITLES:
        return ID_TITLES[key]
    if key.startswith("id-"):
        key = key[3:].replace("-", " ")
        return key[:1].upper() + key[1:] if key else raw
    return raw

from __future__ import unicode_literals

import random

from datetime import date

from scoodent.models import (
    TReportEnum, Student, Report,
    Discipline, StudentGroup
)


def get_random_date(start, end):
    """Random date from datetime.date range.

    :param datetime.date start: left limit
    :param datetime.date end: right limit
    :return: random datetime.date from range
    """

    return date.fromordinal(random.randint(start.toordinal(), end.toordinal()))


def random_name():
    """Return random name.

    :rtype: str
    """

    return random.choice([
        "Жожа", "Авраам", "Вильгельм", "Азис", "Абстракт", "Иона", "Варган",
        "Бенжамин", "Анубис-гер-Метрономус", "Пётр", "Вектор", "Виктор",
        "Перегей"
    ])


def random_surname():
    """Return random surname.

    :rtype: str
    """

    return random.choice([
        "Фурриганов", "Пертрпровский-Розмаринов", "Керамич", "Копыч", "Бро",
        "Ганзинский", "Исмаислёв", "Ашмак-вэчетыре", "Амазонов", "Березовский",
        "Петров"
    ])


def random_birthdate():
    """Random approximate birthdate.

    :return: random datetime.date from range
    """

    start = date(1992, 1, 1)
    end = date(2000, 12, 30)

    return get_random_date(start, end)


def random_pass_date():
    """Return random date for report."""

    ranges = [
        ((2014, 12, 15), (2014, 12, 28)),
        ((2015, 5, 15), (2015, 5, 28)),
        ((2015, 12, 15), (2015, 12, 28)),
        ((2016, 5, 15), (2016, 5, 28)),
        ((2016, 12, 15), (2016, 12, 28)),
    ]

    start, end = random.choice(ranges)
    return get_random_date(date(*start), date(*end))


def random_address():
    """Random address.

    :rtype: str
    """

    return random.choice([
        "г. Москва, ул. Лобызова, д. {0} кв. {1}",
        "г. Москва, ул. Морозная, д. {0} кв. {1}",
        "г. Москва, ул. Маршалла Алигнмента, д. {0} кв. {1}",
        "г. Москва, ул. Первая-2, д. {0} кв. {1}",
        "г. Москва, ул. Новомосковское ш., д. {0} кв. {1}",
        "г. Пенза, ул. Ленина, д. {0} кв. {1}",
        "г. Октябрьск, ул. Ленина, д. {0} кв. {1}",
        "г. Кемерово, ул. Ленина, д. {0} кв. {1}",
        "г. Окск-на-волге, ул. Ленина, д. {0} кв. {1}",
        "г. Дзержинск, ул. Ленина, д. {0} кв. {1}",
        "г. Краснознаменск, ул. Дообедова, д. {0} кв. {1}",
        "г. Москва, ул. 5-й квартал Капотни, д. {0} кв. {1}",
        ]).format(random.randint(1, 160), random.randint(1, 200))


def random_phone():
    return "+7({0}){1}-{2}-{3}".format(
        random.randint(900, 999),
        random.randint(100, 999),
        random.randint(10, 99),
        random.randint(10, 99))


def random_student():
    student = {
        "name": random_name(),
        "surname": random_surname(),
        "birthdate": random_birthdate(),
        "address": random_address(),
        "phone": random_phone(),
        "parents_phone": random_phone(),
        "school": "Школа №{0}".format(random.randint(1, 1800)),
    }
    enter_date = student["birthdate"]
    enter_date.replace(year=enter_date.year + 17, month=9, day=1)
    student["enter_date"] = enter_date

    return student


def random_report():
    """Return random report."""

    return {
        "mark": random.randint(2, 6),
        "mark_date": random_pass_date(),
        "report_type": random.choice(TReportEnum._fields),
    }


def get_disciplines():
    """Return disciplines tuple."""

    return (
        "Математический анализ",
        "ИКТ и ПБРОБЗ 4 ГРОСУ",
        "Интеллект машин БСУИТ",
        "ИИ и ИИИ",
        "Физика ч.4",
        "Теоритическая полемика топономий",
        "Философия древнего мира",
        "История",
        "Робототехника",
        "Теория цепных цепей Марка Ву",
        "Аналитическая геометрия на местности",
    )


def get_groups():
    """Return groups tuple."""

    return (
        ("РГУТАМИ-16-1", False),
        ("ИТБОНСУ-16-1", False),
        ("ГОДЗАИ-16-2", True),
        ("ИМАСУ-15-8", True)
    )


def generate_data(session):
    """Generate testing data and fill DB via session."""

    students = (random_student() for _ in range(20))

    disciplines = list(map(lambda it: Discipline(name=it), get_disciplines()))
    session.add_all(disciplines)
    session.commit()

    groups = list(
        map(lambda it: StudentGroup(name=it[0], fulltime=it[1]), get_groups()))
    session.add_all(groups)
    session.commit()

    for student in students:
        group = random.choice(groups)
        student["student_group"] = group
        student = Student(**student)

        report = random_report()
        report["student"] = student
        report["discipline"] = random.choice(disciplines)

        session.add(Report(**report))
        session.add(student)

    session.commit()

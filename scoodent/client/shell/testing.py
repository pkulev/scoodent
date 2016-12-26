from __future__ import unicode_literals

# import json
import random

from datetime import date  # , timedelta

# from scoodent.common import config
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


# def get_appartaments(places, percent):
#     """Return type of appartaments by percentage.

#     :param list places: list of places
#     :param int percent: current client percentage
#     :return: place dict
#     """

#     if 0 <= percent <= 50:
#         category = CategoryEnum.half_lux
#     elif 50 < percent <= 90:
#         category = CategoryEnum.lux
#     else:
#         category = CategoryEnum.appartaments

#     return random.choice(
#         list(filter(lambda item: item.category == category, places)))


# def get_cost(category, days=1):
#     category_cost_map = {
#         CategoryEnum.half_lux: 3000 * days,
#         CategoryEnum.lux: 5000 * days,
#         CategoryEnum.appartaments: 7000 * days
#     }
#     return category_cost_map[category]


# def get_departure_days(percent):
#     """Return days due departure by percentage."""

#     if 0 <= percent <= 50:
#         days = 7
#     elif 50 < percent <= 70:
#         days = 10
#     elif 70 < percent <= 90:
#         days = 14
#     else:
#         days = 21
#     return days


# def get_departure_date(incoming_date, percent):
#     """Return departure data by percentage.

#     :rtype: datetime.date
#     """

#     days = get_departure_days(percent)
#     return incoming_date + timedelta(days=days)


# def get_real_departure_date(ticket, percent):
#     """Return real departure date by percentage."""

#     def get_departure_days(_, __):
#         """Monkeypatch to use in get_departure_date."""

#         return random.randint(-5, -1)

#     if 0 <= percent <= 3:
#         return None
#     elif 3 < percent <= 15:
#         return get_departure_date(ticket.departure_date, percent)
#     else:
#         return ticket.departure_date


# def json_without_id(path):
#     """Parse json and return data without id."""

#     with open(path, "r") as source:
#         data = json.load(source)
#     list(map(lambda it: it.pop("id"), data))
#     return data


# def generate_data(session):
#     """Generate testing data and fill DB via session."""

#     places = list(map(
#         lambda place: Place(**place),
#         json_without_id(config.MOCK["place"])))
#     session.add_all(places)
#     session.commit()

#     organisations = list(map(
#         lambda organisation: Organisation(**organisation),
#         json_without_id(config.MOCK["organisation"])))
#     session.add_all(organisations)
#     session.commit()

#     clients = list(map(
#         lambda client: Client(**client),
#         json_without_id(config.MOCK["client"])))

#     current_client = 0
#     current_table = 1
#     table_capacity = 4
#     current_table_free = table_capacity

#     for client in clients:
#         current_client += 1
#         current_percent = current_client * len(clients) / 100

#         start_date = date.today().replace(month=date.today().month - 2)
#         today = date.today()
#         two_month_after = today.replace(month=today.month + 2)

#         appartaments = get_appartaments(places, current_percent)

#         # order date = random date from (today - 2 month) until now
#         ticket_fields = {
#             "client": client,
#             "place": appartaments,
#             "order_date": get_random_date(start_date, today),
#             "cost": get_cost(
#                 appartaments.category, get_departure_days(current_percent))
#         }

#         # incoming_date = randrom from order_date + 2 month
#         ticket_fields["incoming_date"] = get_random_date(
#             ticket_fields["order_date"], two_month_after)

#         # departure_date = incoming_date + days by percentage
#         ticket_fields["departure_date"] = get_departure_date(
#             ticket_fields["incoming_date"], current_percent)

#         if current_client % 5 == 0:
#             ticket_fields["organisation"] = random.choice(organisations)

#         # table allocation
#         ticket_fields["table_num"] = current_table
#         current_table_free -= 1
#         if current_table_free == 0:
#             current_table_free = table_capacity
#             current_table += 1

#         ticket = Ticket(**ticket_fields)

#         # departure table generation
#         departure_fields = {
#             "ticket": ticket,
#             "departure_date": get_real_departure_date(ticket, current_percent)
#         }

#         if current_percent <= 3:
#             departure_fields["incoming_date"] = None
#             departure_fields["early_departure_reason"] = "did not come"
#         elif current_percent <= 15:
#             departure_fields["early_departure_reason"] = "circumstances"
#             departure_fields["incoming_date"] = ticket.incoming_date
#         else:
#             departure_fields["incoming_date"] = ticket.incoming_date

#         session.add(client)
#         session.add(ticket)
#         session.add(Departure(**departure_fields))
#     session.commit()

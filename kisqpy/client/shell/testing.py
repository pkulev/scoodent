import json
import random

from datetime import date, timedelta

from kisqpy.common import config
from kisqpy.models import (
    Client, CategoryEnum, Departure, Organisation, Place, Ticket
)


def get_appartaments(places, percent):
    """Return type of appartaments by percentage.

    :param list places: list of places
    :param int percent: current client percentage
    :return: place dict
    """


    if 0 <= percent <= 50:
        category = CategoryEnum.half_lux
    elif 50 < percent <= 90:
        category = CategoryEnum.lux
    else:
        category = CategoryEnum.appartaments

    return random.choice(
        list(filter(lambda item: item.category == category, places)))


def get_cost(category, days=1):
    category_cost_map = {
        CategoryEnum.half_lux: 3000 * days,
        CategoryEnum.lux: 5000 * days,
        CategoryEnum.appartaments: 7000 * days
    }
    return category_cost_map[category]


def get_random_date(start, end):
    """Random date from datetime.date range.

    :param datetime.date start: left limit
    :param datetime.date end: right limit
    :return: random datetime.date from range
    """

    return date.fromordinal(random.randint(start.toordinal(), end.toordinal()))


def get_departure_days(percent):
    """Return days due departure by percentage."""

    if 0 <= percent <= 50:
        days = 7
    elif 50 < percent <= 70:
        days = 10
    elif 70 < percent <= 90:
        days = 14
    else:
        days = 21
    return days


def get_departure_date(incoming_date, percent):
    """Return departure data by percentage.

    :rtype: datetime.date
    """

    days = get_departure_days(percent)
    return incoming_date + timedelta(days=days)


def get_real_departure_date(ticket, percent):
    """Return real departure date by percentage."""

    def get_departure_days(_, __):
        """Monkeypatch to use in get_departure_date."""

        return random.randint(-5, -1)

    if 0 <= percent <= 3:
        return None
    elif 3 < percent <= 15:
        return get_departure_date(ticket.departure_date, percent)
    else:
        return ticket.departure_date


def json_without_id(path):
    """Parse json and return data without id."""

    with open(path, "r") as source:
        data = json.load(source)
    map(lambda it: it.pop["id"], data)
    return data


def generate_data(session):
    """Generate testing data and fill DB via session."""

    places = list(map(
        lambda place: Place(**place),
        json_without_id(config.MOCK["place"])))
    session.add_all(places)
    session.commit()

    organisations = list(map(
        lambda organisation: Organisation(**organisation),
        json_without_id(config.MOCK["organisation"])))
    session.add_all(organisations)
    session.commit()

    clients = list(map(
        lambda client: Client(**client),
        json_without_id(config.MOCK["client"])))

    current_client = 0
    current_table = 1
    table_capacity = 4
    current_table_free = table_capacity

    for client in clients:
        current_client += 1
        current_percent = current_client * len(clients) / 100

        start_date = date.today().replace(month=date.today().month - 2)
        today = date.today()
        two_month_after = today.replace(month=today.month + 2)

        appartaments = get_appartaments(places, current_percent)

        # order date = random date from (today - 2 month) until now
        ticket_fields = {
            "place_id": appartaments.id,
            "order_date": get_random_date(start_date, today),
            "cost": get_cost(
                appartaments.category, get_departure_days(current_percent))
        }

        # incoming_date = randrom from order_date + 2 month
        ticket_fields["incoming_date"] = get_random_date(
            ticket_fields["order_date"], two_month_after)

        # departure_date = incoming_date + days by percentage
        ticket_fields["departure_date"] = get_departure_date(
            ticket_fields["incoming_date"], current_percent)

        if current_client % 5 == 0:
            ticket_fields["org_id"] = random.choice(organisations).id

        # table allocation
        ticket_fields["table_num"] = current_table
        current_table_free -= 1
        if current_table_free == 0:
            current_table_free = table_capacity
            current_table += 1

        ticket = Ticket(**ticket_fields)

        # departure table generation
        departure_fields = {
            "client_id": client.id,
            "ticket_id": ticket.id,
            "departure_date": get_real_departure_date(ticket, current_percent)
        }

        if current_percent <= 3:
            departure_fields["incoming_date"] = None
            departure_fields["early_dep_reason"] = "did not come"
        elif current_percent <= 15:
            departure_fields["early_dep_reason"] = "circumstances"
            departure_fields["incoming_date"] = ticket.incoming_date
        else:
            departure_fields["incoming_date"] = ticket.incoming_date

        session.add(client)
        session.commit()
        session.add(ticket)
        session.add(Departure(**departure_fields))
        session.commit()

    # client = Client(first_name="Tasty", last_name="Tester")
    # session.add(client)
    # session.commit()

    # session.add(Address(post_code="00000", client=client))
    # session.commit()

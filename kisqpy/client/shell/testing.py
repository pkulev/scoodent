import json
import random

from datetime import date, timedelta

from kisqpy.common import config
from kisqpy.models import (
    Client, CategoryEnum, Departure, Organisation, Place, Ticket
)


def get_appartaments(client_num, places, total):
    """Return type of appartaments."""

    percent = client_num * total / 100

    if 0 <= percent <= 50:
        cat = CategoryEnum.half_lux
    elif 50 < percent <= 90:
        cat = CategoryEnum.lux
    else:
        cat = CategoryEnum.appartaments

    return random.choice(filter(lambda it: it["cat"] == cat, places))


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


def get_departure_days(client_num, total):
    percent = client_num * total / 100

    if 0 <= percent <= 50:
        days = 7
    elif 50 < percent <= 70:
        days = 10
    elif 70 < percent <= 90:
        days = 14
    else:
        days = 21
    return days


def get_departure_date(client_num, incoming_date, total):

    days = get_departure_days(client_num, total)
    return incoming_date + timedelta(days=days)


def generate_data(session):

    with open(config.MOCK["place"], "r") as source:
        places = json.load(source)
    session.add_all([Place(**place) for place in places])
    session.commit()

    with open(config.MOCK["client"], "r") as source:
        clients = json.load(source)

    with open(config.MOCK["organisation"], "r") as source:
        organisations = json.load(source)

    for organisation in organisations:
        session.add(Organisation(**organisation))
        session.commit()

    client_counter = 0

    for client in clients:
        new_client = Client(**client)
        client_counter += 1

        current_table = 1
        table_capacity = 4
        current_table_free = table_capacity

        start_date = date.today().replace(month=date.today().month - 2)
        today = date.today()
        two_month_after = today.replace(month=today.month + 2)

        appartaments = get_appartaments(client_counter, places, len(clients))

        # order date = random date from (today - 2 month) until now
        ticket_fields = {
            "place_id": appartaments["id"],
            "order_date": get_random_date(start_date, today),
            "cost": get_cost(appartaments["cat"], get_departure_days(
                client_counter, len(clients)))
        }

        # incoming_date = randrom from order_date + 2 month
        ticket_fields["incoming_date"] = get_random_date(
            ticket_fields["order_date"], two_month_after)

        # departure_date = incoming_date + days by percentage
        ticket_fields["departure_date"] = get_departure_date(
            client_counter, ticket_fields["incoming_date"], len(clients))

        if client_counter % 5 == 0:
            ticket_fields["org_id"] = random.choice(organisations)["id"]

        # table allocation
        ticket_fields["table_num"] = current_table
        current_table_free -= 1
        if current_table_free == 0:
            current_table_free = table_capacity
            current_table += 1

        session.add(new_client)
        session.add(Ticket(**ticket_fields))
        session.commit()

    # new_client = Client(first_name="Tasty", last_name="Tester")
    # session.add(new_client)
    # session.commit()

    # session.add(Address(post_code="00000", client=new_client))
    # session.commit()


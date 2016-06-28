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

    return random.choice(filter(lambda it: it["cat"] == cat, places))["id"]


def get_random_date(start, end):
    """Random date from datetime.date range.

    :param datetime.date start: left limit
    :param datetime.date end: right limit
    :return: random datetime.date from range
    """

    return date.fromordinal(random.randint(start.toordinal(), end.toordinal()))


def get_departure_date(client_num, incoming_date, total):
    percent = client_num * total / 100

    if 0 <= percent <= 50:
        days = 7
    elif 50 < percent <= 70:
        days = 10
    elif 70 < percent <= 90:
        days = 14
    else:
        days = 21
    return incoming_date + timedelta(days=days)


def generate_data(session):

    with open(config.MOCK["client"], "r") as source:
        clients = json.load(source)

    with open(config.MOCK["place"], "r") as source:
        places = json.load(source)

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

        start_date = date.today().replace(month=date.today().month - 2)
        today = date.today()
        two_month_after = today.replace(month=today.month + 2)

        # order date = random date from (today - 2 month) until now
        ticket_fields = {
            "place_id": get_appartaments(client_counter, places, len(clients)),
            "order_date": get_random_date(start_date, today)
        }

        # incoming_date = randrom from order_date + 2 month
        ticket_fields["incoming_date"] = get_random_date(
            ticket_fields["order_date"], two_month_after)

        # departure_date = incoming_date + days by percentage
        ticket_fields["departure_date"] = get_departure_date(
            client_counter, ticket_fields["incoming_date"], len(clients))

        if client_counter % 5 == 0:
            ticket_fields["org_id"] = random.choise(organisations)["id"]

        session.add(new_client)
        session.add(Ticket(**ticket_fields))
        session.commit()

    # new_client = Client(first_name="Tasty", last_name="Tester")
    # session.add(new_client)
    # session.commit()

    # session.add(Address(post_code="00000", client=new_client))
    # session.commit()


#!/usr/bin/env python

"""Create initial database schema."""

import argparse
import json
import random
import sys
from datetime import date, timedelta

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from kisqpy.common import config
from kisqpy.models import (
    Base, Client, CategoryEnum, ClientTicketMap,
    Departure, Organisation, Place, Ticket
)


def create_schema(args):
    """Create initial schema."""

    if not args.yes:
        return

    engine = create_engine(config.DB_URI, echo=config.DEBUG)
    Base.metadata.create_all(engine)


def delete_schema(args):
    """Delete schema."""

    if not args.yes:
        return

    engine = create_engine(config.DB_URI, echo=config.DEBUG)
    meta = MetaData(engine)
    meta.reflect()
    meta.drop_all()


def create_testing(args):
    """Fill database by testing entities."""

    if not args.yes:
        return

    engine = create_engine(config.DB_URI, echo=config.DEBUG)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    with open(config.MOCK["client"], "r") as source:
        clients = json.load(source)

    with open(config.MOCK["place"], "r") as source:
        places = json.load(source)

    with open(config.MOCK["organisation"], "r") as source:
        organisations = json.load(source)

    for organisation in organisations:
        session.add(Organisation(**organisation))
        session.commit()

    def get_appartaments(client_num, total=len(clients)):
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

        return date.fromordinal(
            random.randint(start.toordinal(), end.toordinal()))

    def get_departure_date(client_num, incoming_date, total=len(clients)):
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
            "place_id": get_appartaments(client_counter),
            "order_date": get_random_date(start_date, today)
        }

        # incoming_date = randrom from order_date + 2 month
        ticket_fields["incoming_date"] = get_random_date(
            ticket_fields["order_date"], two_month_after)

        # departure_date = incoming_date + days by percentage
        ticket_fields["departure_date"] = get_departure_date(
            client_counter, ticket_fields["incoming_date"])

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


def parse_args():
    """Parse incoming arguments."""

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # sub_drop = subparsers.add_parser("drop", help="drop selected DB")
    # sub_drop.add_argument("dbname", help="DB name to drop")

    sub_schema = subparsers.add_parser("schema", help="create DB schema")
    sub_schema.add_argument("--yes", action="store_true", help="really create")
    sub_schema.set_defaults(func=create_schema)

    sub_delete_schema = subparsers.add_parser("dropall", help="drop all tables")
    sub_delete_schema.add_argument("--yes", action="store_true", help="really drop")
    sub_delete_schema.set_defaults(func=delete_schema)

    sub_testing = subparsers.add_parser("testing", help="fill DB by some data")
    sub_testing.add_argument(
        "--yes", action="store_true", help="really create")
    sub_testing.set_defaults(func=create_testing)

    args = parser.parse_args()
    return args


def main():
    """Entry point."""

    args = parse_args()
    if "func" in args:
        args.func(args)
    else:
        sys.exit("Invalid command")

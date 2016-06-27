#!/usr/bin/env python

"""Create initial database scheme."""

import argparse
import json
import sys

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from kisqpy.common import config
from kisqpy.models import (
    Base, Client, ClientTicketMap, Departure, Organisation, Place, Ticket
)


def create_scheme(args):
    """Create initial scheme."""

    if not args.yes:
        return

    engine = create_engine(config.DB_URI, echo=config.DEBUG)
    Base.metadata.create_all(engine)


def delete_scheme(args):
    """Delete scheme."""

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

    for client in clients:
        new_client = Client(**client)
        session.add(new_client)
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

    sub_scheme = subparsers.add_parser("scheme", help="create DB scheme")
    sub_scheme.add_argument("--yes", action="store_true", help="really create")
    sub_scheme.set_defaults(func=create_scheme)

    sub_delete_scheme = subparsers.add_parser("dropall", help="drop all tables")
    sub_delete_scheme.add_argument("--yes", action="store_true", help="really drop")
    sub_delete_scheme.set_defaults(func=delete_scheme)

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

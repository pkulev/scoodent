#!/usr/bin/env python

"""Create initial database scheme."""

import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kisqpy.common import config
from kisqpy.models import Base, Client, Address


def create_scheme(args):
    """Create initial scheme."""

    if not args.yes:
        return

    engine = create_engine(config.DB_URI)
    Base.metadata.create_all(engine)


def create_testing(args):
    """Fill database by testing entities."""

    if not args.yes:
        return

    engine = create_engine(config.DB_URI)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    new_client = Client(first_name="Tasty", last_name="Tester")
    session.add(new_client)
    session.commit()

    session.add(Address(post_code="00000", client=new_client))
    session.commit()


def parse_args():
    """Parse incoming arguments."""

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # sub_drop = subparsers.add_parser("drop", help="drop selected DB")
    # sub_drop.add_argument("dbname", help="DB name to drop")

    sub_scheme = subparsers.add_parser("scheme", help="create DB scheme")
    sub_scheme.add_argument("--yes", action="store_true", help="really create")
    sub_scheme.set_defaults(func=create_scheme)

    sub_testing = subparsers.add_parser("testing", help="fill DB by some data")
    sub_testing.add_argument(
        "--yes", action="store_true", help="really create")
    sub_testing.set_defaults(func=create_testing)

    args = parser.parse_args()
    return args


def main():
    """Entry point."""

    args = parse_args()
    args.func(args)

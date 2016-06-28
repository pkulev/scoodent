#!/usr/bin/env python

"""Create initial database schema."""

import argparse
import sys

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from kisqpy.common import config
from kisqpy.models import Base
from kisqpy.client.shell import testing


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
    testing.generate_data(DBSession())


# TODO: refactor
# prog db drop -y --yes + interactive
# prog db drop -d --dry-run
# prog db create --schema -y
# prog db insert --testing -y
# prog db show -t --table [name]
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

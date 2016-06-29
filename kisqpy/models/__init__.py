"""Kisqpy models."""

from collections import namedtuple
from decimal import Decimal

from sqlalchemy import (
    Column, Date, Enum, ForeignKey, Integer, String, Text
)
from sqlalchemy.types import UserDefinedType
from sqlalchemy.orm import relationship

from kisqpy.common.db import Base


_Category = namedtuple("CategoryEnumType", ["half_lux", "lux", "appartaments"])
"""Represents Category enum type."""

CategoryEnum = _Category("half-lux", "lux", "appartaments")
"""Category mapping."""

Category = Enum(
    CategoryEnum.half_lux,
    CategoryEnum.lux,
    CategoryEnum.appartaments,
    name="category")


class Money(UserDefinedType):
    """PostgreSQL MONEY type."""

    def get_col_spec(self):
        return "money"

    def result_processor(self, dialect, colltype):
        def process(value):
            if value.startswith("-"):
                trimpoint = 2
                sign = "-"
            else:
                trimpoint = 1
                sign = ""

            return Decimal(sign + value[trimpoint:].replace(",", ""))
        return process


class Client(Base):
    """Client DAO representation."""

    __tablename__ = "client"

    id = Column(Integer, primary_key=True, unique=True)
    surname = Column(String(64), nullable=False)
    name = Column(String(64), nullable=False)
    birthdate = Column(Date, nullable=False)
    city = Column(String(64), nullable=False)
    street = Column(String(64), nullable=False)
    phone = Column(String(32), nullable=False)


class ClientTicketMap(Base):
    """Client room mapping."""

    __tablename__ = "client_ticket_map"

    client_id = Column(Integer, ForeignKey("client.id"), primary_key=True, unique=True)
    ticket_id = Column(Integer, ForeignKey("ticket.id"), primary_key=True, unique=True)
    client = relationship("Client")
    ticket = relationship("Ticket")


class Departure(Base):
    """Departure DAO representation."""

    __tablename__ = "departure"

    id = Column(Integer, primary_key=True, unique=True)
    client_id = Column(Integer, ForeignKey("client.id"), unique=True)
    ticket_id = Column(Integer, ForeignKey("ticket.id"), unique=True)
    incoming_date = Column(Date)
    departure_date = Column(Date)
    early_dep_reason = Column(Text)
    client = relationship("Client")
    ticket = relationship("Ticket")


class Organisation(Base):
    """Organisation DAO representation."""

    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(128), nullable=False)


class Place(Base):
    """Place DAO representation."""

    __tablename__ = "place"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(64), nullable=False)
    room = Column(Integer, nullable=False)
    category = Column(Category, nullable=False)


class Ticket(Base):
    """Ticket DAO representation."""

    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True, unique=True)
    org_id = Column(Integer, ForeignKey("organisation.id"))
    place_id = Column(Integer, ForeignKey("place.id"))
    order_date = Column(Date, nullable=False)
    incoming_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    table_num = Column(Integer, nullable=False)
    cost = Column(Money, nullable=False)
    organisation = relationship("Organisation")
    place = relationship("Place")

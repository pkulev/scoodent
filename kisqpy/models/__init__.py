"""Kisqpy models."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


__all__ = ["Base", "Client", "Address"]


Base = declarative_base()


class Client(Base):
    """Client DAO representation."""

    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)


class Address(Base):
    """Address DAO representation."""

    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    street_name = Column(String(64))
    street_number = Column(String(64))
    post_code = Column(String(64), nullable=False)
    client_id = Column(Integer, ForeignKey("client.id"))
    client = relationship(Client)

"""DB utils and helpers."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from kisqpy.common import config


Base = declarative_base()


def get_engine(debug=None):
    """Return ORM engine."""

    debug = config.DEBUG if debug is None else debug
    return create_engine(config.DB_URI, echo=debug)


def get_session(debug=None):
    """Return DB session."""

    engine = get_engine(debug)
    Base.metadata.bind = engine
    return sessionmaker(bind=engine)()


def insert_objects(obj):
    """Insert object or objects to DB."""

    session = get_session()
    if isinstance(obj, (tuple, list)):
        session.add_all(obj)
    else:
        session.add(obj)
    session.commit()

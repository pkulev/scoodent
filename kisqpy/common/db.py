"""DB utils and helpers."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from kisqpy.common import config


def get_engine(debug=None):
    """Return ORM engine."""

    return create_engine(config.DB_URI, echo=debug or config.DEBUG)


def get_session(base, debug=None):
    """Return DB session."""

    engine = get_engine(debug)
    base.metadata.bind = engine
    return sessionmaker(bind=engine)()

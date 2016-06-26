"""Client configuration."""

import os

from kisqpy.common import constants


DEBUG = True
"""Global debug mode."""


DBAPI = constants.DBAPI_POSTGRES
"""Database API."""


DB_URI_TPL = "{schema}+{driver}://{user}:{password}@{host}:{port}/{dbname}"
"""Database URI template."""


DB_URIS = {
    constants.DBAPI_POSTGRES: {
        "schema": constants.DBAPI_POSTGRES,
        "driver": constants.DBDRIVER_PSYCOPG2,
        "user": os.environ["USER"],
        "password": os.environ.get("KISQPY_DB_PASS", ""),
        "host": os.environ.get("KISQPY_DB_HOST", "localhost"),
        "port": int(os.environ.get("KISQPY_DB_PORT", 5432)),
        "dbname": constants.DB_NAME
    }
}


DB_URI = DB_URI_TPL.format(**DB_URIS[DBAPI])
"""Database Unified Resource Locator."""

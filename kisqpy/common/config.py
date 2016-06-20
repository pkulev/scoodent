"""Client configuration."""


import os


DB_NAME = "hotel"
"""Application database name."""


DBAPI = "postgresql"
"""Database API."""


_DB_URI_TPL = "{schema}+{driver}://{user}:{password}@{host}:{port}/{dbname}"
"""Database URI template."""


_DB_URIS = {
    "postgresql": {
        "schema": "postgresql",
        "driver": "psycopg2",
        "user": os.environ["USER"],
        "password": os.environ.get("KISQPY_DB_PASS", ""),
        "host": os.environ.get("KISQPY_DB_HOST", "localhost"),
        "port": int(os.environ.get("KISQPY_DB_PORT", 5432)),
        "dbname": DB_NAME
    }
}


DB_URI = _DB_URI_TPL.format(**_DB_URIS[DBAPI])
"""Database Unified Resource Locator."""

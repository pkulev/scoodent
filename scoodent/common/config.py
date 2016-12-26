"""Client configuration."""

import os
from functools import partial

import scoodent
from scoodent.common import constants


DEBUG = True
"""Global debug mode."""


DBAPI = constants.DBAPI_POSTGRES
"""Database API."""


# DB_URI_TPL =
# """Database URI template."""


DB_URIS = {
    constants.DBAPI_POSTGRES: {
        "uri": "{schema}+{driver}://{user}:{password}@{host}:{port}/{dbname}",
        "options": {
            "schema": constants.DBAPI_POSTGRES,
            "driver": constants.DBDRIVER_PSYCOPG2,
            "user": os.environ["USER"],
            "password": os.environ.get("SCOODENT_DB_PASS", ""),
            "host": os.environ.get("SCOODENT_DB_HOST", "localhost"),
            "port": int(os.environ.get("SCOODENT_DB_PORT", 5432)),
            "dbname": constants.DB_NAME,
        },
    },
    constants.DBAPI_SQLITE: {
        "uri": "{schema}+{driver}://{user}:{password}@{host}:{port}/{dbname}",
        "options": {
            "schema": constants.DBAPI_SQLITE,
            "host": os.environ.get("SCOODENT_DB_HOST", "localhost"),
        },
    },
}
"""Database URI config."""


DB_URI = DB_URIS[DBAPI]["uri"].format(**DB_URIS[DBAPI]["options"])
# DB_URI_TPL.format(**DB_URIS[DBAPI])
# """Database Unified Resource Locator."""


ROOT = os.path.dirname(scoodent.__file__)
"""Project's root path."""

UI_DIR = partial(os.path.join, os.path.join(ROOT, "client"))
"""Helper partial."""

UI = {
    "main": UI_DIR("main.ui"),
    "student_dialog": UI_DIR("student_dialog.ui"),
    "report_dialog": UI_DIR("report_dialog.ui"),
    "discipline_dialog": UI_DIR("discipline_dialog.ui"),
    "group_dialog": UI_DIR("group_dialog.ui"),
}
"""Widget <-> path to .ui mapping."""

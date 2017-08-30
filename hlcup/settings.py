# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging
import sqlite3

import os
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool

logger = logging.getLogger(__name__)

BULK_INSERT_SIZE = 200000
MEMORY_BASED = int(os.environ.get('INMEMORY', 1))
DUMMY_API = int(os.environ.get('DUMMY_API', 0))
SMALL_DATA = int(os.environ.get('SMALL_DATA', 1))
JAPRONTO_PORT = int(os.environ.get('JAPRONTO_PORT', 8000))
JAPRONTO_HOST = os.environ.get('JAPRONTO_HOST', '0.0.0.0')
WORKER_NUM = int(os.environ.get('WORKER_NUM', 1))
DB_PATH = '/tmp/hlcup.db'

PATH_TO_ZIP = '/tmp/data/data_small.zip' if SMALL_DATA else '/tmp/data/data.zip'

logger.info('MEMORY_BASED={}'.format(MEMORY_BASED))


def sqlite_based():
    creator = lambda: sqlite3.connect(DB_PATH)
    return create_engine('sqlite://', creator=creator)


def sqlite_mem_based():
    return create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode = MEMORY")
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA cache_size = 100000")
    cursor.execute("PRAGMA temp_store = MEMORY")
    cursor.execute("PRAGMA count_changes = OFF")
    cursor.close()


engine = sqlite_mem_based() if MEMORY_BASED else sqlite_based()
Session = sessionmaker(bind=engine)
# Session = scoped_session(Session)

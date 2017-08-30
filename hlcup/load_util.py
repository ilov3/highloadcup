# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging
import os
import ujson
from functools import partial
from time import time
from zipfile import ZipFile

import itertools

from hlcup.models import User, Location, Visit, create_all_indexes
from hlcup.models.base import create_schema
from hlcup.settings import PATH_TO_ZIP, engine, BULK_INSERT_SIZE, DB_PATH

logger = logging.getLogger(__name__)


def load_data():
    def grouper(n, iterable, fillvalue=None):
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    extract_data = lambda txt: (ujson.loads(zip_file.read(n)).popitem() for n in
                                filter(lambda name: os.path.basename(name).startswith(txt), namelist))
    create_schema()
    zip_file = ZipFile(PATH_TO_ZIP)
    namelist = zip_file.namelist()
    users_data = (item for key, items in extract_data('user') for item in items)
    locations_data = (item for key, items in extract_data('location') for item in items)
    visits_data = (item for key, items in extract_data('visit') for item in items)
    load_users_func = partial(load_to_db, User)
    load_locations_func = partial(load_to_db, Location)
    load_visits_func = partial(load_to_db, Visit)
    logger.info('Loading data...')
    start = time()
    list(map(load_users_func, (chunk for chunk in grouper(BULK_INSERT_SIZE, users_data))))
    t1 = time()
    logger.info('Users loaded. Took: {} secs.'.format(time() - start))
    list(map(load_locations_func, (chunk for chunk in grouper(BULK_INSERT_SIZE, locations_data))))
    t2 = time()
    logger.info('Locations loaded. Took: {} secs.'.format(time() - t1))
    list(map(load_visits_func, (chunk for chunk in grouper(BULK_INSERT_SIZE, visits_data))))
    logger.info('Visits loaded. Took: {} secs.'.format(time() - t2))
    logger.info('Data loaded. Took: {} secs.'.format(time() - start))
    logger.info('Creating indexes')
    t3 = time()
    create_all_indexes(engine)
    logger.info('Indexes created. Took: {}'.format(time() - t3))


def load_to_db(model, items):
    engine.execute(model.__table__.insert(), list(filter(lambda item: item, items)))


if __name__ == '__main__':
    try:
        os.remove(DB_PATH)
    except Exception:
        pass
    load_data()

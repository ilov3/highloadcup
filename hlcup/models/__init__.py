# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging
from .location import Location, create_indexes as create_location_indexes
from .user import User, create_indexes as create_user_indexes
from .visit import Visit, create_indexes as create_visit_indexes

logger = logging.getLogger(__name__)

__all__ = [
    'Location',
    'Visit',
    'User',
    'create_all_indexes',
]


def create_all_indexes(engine):
    create_user_indexes(engine)
    create_location_indexes(engine)
    create_visit_indexes(engine)

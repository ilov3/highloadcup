# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging

from sqlalchemy import Column, Integer, String, Index

from hlcup.models.base import Base

logger = logging.getLogger(__name__)


class Location(Base):
    place = Column(String(255), nullable=False)
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    distance = Column(Integer(), nullable=False)


def create_indexes(engine):
    Index('location_country_idx', Location.country).create(bind=engine)
    Index('location_distance_idx', Location.distance).create(bind=engine)

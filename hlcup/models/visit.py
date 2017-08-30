# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging

from sqlalchemy import Column, ForeignKey, Integer, Index

from hlcup.models.base import Base

logger = logging.getLogger(__name__)


class Visit(Base):
    user = Column(None, ForeignKey('user.id'), nullable=False)
    location = Column(None, ForeignKey('location.id'), nullable=False)
    visited_at = Column(Integer, nullable=False)
    mark = Column(Integer, nullable=False)


def create_indexes(engine):
    Index('visit_user_idx', Visit.user).create(bind=engine)
    Index('visit_location_idx', Visit.location).create(bind=engine)
    Index('visit_visited_at_idx', Visit.visited_at).create(bind=engine)
    Index('visit_mark_idx', Visit.mark).create(bind=engine)

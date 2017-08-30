# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging

from sqlalchemy import Column, String, Integer, Index

from hlcup.models.base import Base

logger = logging.getLogger(__name__)


class User(Base):
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    gender = Column(String(1), nullable=False)
    email = Column(String(50), nullable=False)
    birth_date = Column(Integer, nullable=False)


def create_indexes(engine):
    Index('user_gender_idx', User.gender).create(bind=engine)
    Index('user_birthdate_idx', User.birth_date).create(bind=engine)

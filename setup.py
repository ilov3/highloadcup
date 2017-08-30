# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging

from setuptools import setup

logger = logging.getLogger(__name__)

setup(
    name='hlcup',
    version='0.1',
    packages=['hlcup', 'hlcup.api', 'hlcup.models'],
    install_requires=[
        'japronto==0.1.1',
        'marshmallow==2.13.6',
        'marshmallow-sqlalchemy==0.13.1',
        'python-dateutil==2.6.1',
        'six==1.10.0',
        'SQLAlchemy==1.1.13',
        'ujson==1.35',
        'uvloop==0.8.0',
    ]
)

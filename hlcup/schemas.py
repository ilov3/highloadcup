# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import Schema, fields

from hlcup.models import User, Location, Visit
from hlcup.validators import get_string_validator, get_int_validator

logger = logging.getLogger(__name__)


class UserSchema(ModelSchema):
    id = fields.Integer(validate=get_int_validator(rank=32))
    first_name = fields.String(validate=get_string_validator(max_length=50))
    last_name = fields.String(validate=get_string_validator(max_length=50))
    email = fields.String(validate=get_string_validator(max_length=50))
    gender = fields.String(validate=get_string_validator(choices=['m', 'f']))
    birth_date = fields.Integer(validate=get_int_validator())

    class Meta:
        model = User


class LocationSchema(ModelSchema):
    id = fields.Integer(validate=get_int_validator(rank=32))
    place = fields.String(validate=get_string_validator())
    country = fields.String(validate=get_string_validator(max_length=50))
    city = fields.String(validate=get_string_validator(max_length=50))
    distance = fields.Integer(validate=get_int_validator(rank=32))

    class Meta:
        model = Location


class VisitSchema(ModelSchema):
    id = fields.Integer(validate=get_int_validator(rank=32))
    user = fields.Integer(validate=get_int_validator(rank=32))
    location = fields.Integer(validate=get_int_validator(rank=32))
    visited_at = fields.Integer(validate=get_int_validator())
    mark = fields.Integer(validate=get_int_validator(_range=[0, 6]))

    class Meta:
        model = Visit


class UserVisitsSchema(Schema):
    mark = fields.Integer()
    visited_at = fields.Integer()
    place = fields.String()

    class Meta:
        model = User


class LocationAvgSchema(Schema):
    avg = fields.Float()

    class Meta:
        model = Location

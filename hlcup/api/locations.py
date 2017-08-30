# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

from marshmallow import ValidationError
from sqlalchemy.sql import func

from hlcup.exceptions import EntityDoesNotExist
from hlcup.models import Location, Visit, User
from hlcup.schemas import LocationSchema
from hlcup.api.helpers import get_entity, GET_HEADERS
from hlcup.settings import Session
from hlcup.validators import get_int_validator, get_string_validator

logger = logging.getLogger(__name__)


def get_location_avg(from_date=None, to_date=None, from_age=None, entity_id=None, to_age=None, gender=None):
    session = Session()
    q = session.query(func.avg(Visit.mark)).join(Location).join(User).filter(Location.id == entity_id)
    if from_date:
        q = q.filter(Visit.visited_at > from_date)
    if to_date:
        q = q.filter(Visit.visited_at < to_date)
    if from_age:
        now = datetime.now() - relativedelta(years=from_age)
        timestamp = calendar.timegm(now.timetuple())
        q = q.filter(User.birth_date < timestamp)
    if to_age:
        now = datetime.now() - relativedelta(years=to_age)
        timestamp = calendar.timegm(now.timetuple())
        q = q.filter(User.birth_date > timestamp)
    if gender:
        q = q.filter(User.gender == gender)
    return q.all()


def location_avg_api(request):
    try:
        entity_id = request.match_dict.get('entity_id')
        entity = get_entity(schema=LocationSchema, entity_id=entity_id)
        from_date = request.query.get('fromDate', None)
        if from_date:
            from_date = get_int_validator()(from_date)
        to_date = request.query.get('toDate', None)
        if to_date:
            to_date = get_int_validator()(to_date)
        from_age = request.query.get('fromAge', None)
        if from_age:
            from_age = get_int_validator()(from_age)
        to_age = request.query.get('toAge', None)
        if to_age:
            to_age = get_int_validator()(to_age)
        gender = request.query.get('gender', None)
        if gender:
            gender = get_string_validator(choices=['m', 'f'])(gender)

        result = get_location_avg(
            entity_id=entity_id,
            from_date=from_date,
            to_date=to_date,
            from_age=from_age,
            to_age=to_age,
            gender=gender,
        )
        if not result[0][0]:
            return request.Response(json={'avg': 0}, code=200, headers=GET_HEADERS)
        avg = round(result[0][0], 5)
        return request.Response(json={'avg': avg}, code=200, headers=GET_HEADERS)
    except EntityDoesNotExist:
        return request.Response(code=404, headers=GET_HEADERS)
    except (ValidationError, AssertionError) as e:
        logger.error(e)
        return request.Response(code=400, headers=GET_HEADERS)

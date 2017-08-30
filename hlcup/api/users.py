# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging

from marshmallow import ValidationError

from hlcup.exceptions import EntityDoesNotExist
from hlcup.models import Visit, Location
from hlcup.schemas import UserSchema, UserVisitsSchema
from hlcup.api.helpers import get_entity, GET_HEADERS
from hlcup.settings import Session
from hlcup.validators import get_string_validator, get_int_validator

logger = logging.getLogger(__name__)


def users_visits_api(request):
    try:
        entity_id = request.match_dict.get('entity_id')
        entity = get_entity(schema=UserSchema, entity_id=entity_id)
        from_date = get_int_validator()(request.query.get('fromDate', 0))
        to_date = get_int_validator()(request.query.get('toDate', 0))
        country = get_string_validator()(request.query.get('country', ''))
        to_distance = get_int_validator()(request.query.get('toDistance', 0))
        session = Session()
        q = session.query(Visit.mark, Visit.visited_at, Location.place).filter(Visit.user == entity_id)
        if from_date:
            q = q.filter(Visit.visited_at > from_date)
        if to_date:
            q = q.filter(Visit.visited_at < to_date)
        if country:
            q = q.filter(Location.country == country)
        if to_distance:
            q = q.filter(Location.distance < to_distance)
        visits = q.join(Location).order_by(Visit.visited_at).all()
        schema = UserVisitsSchema(many=True)
        result = {'visits': schema.dump(visits).data}
        return request.Response(json=result, code=200, headers=GET_HEADERS)
    except EntityDoesNotExist:
        return request.Response(code=404, headers=GET_HEADERS)
    except ValidationError as e:
        logger.error(e)
        return request.Response(code=400, headers=GET_HEADERS)

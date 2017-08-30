# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging
from json import JSONDecodeError

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from hlcup.settings import Session
from hlcup.exceptions import EntityDoesNotExist

logger = logging.getLogger(__name__)

GET_HEADERS = {
    'connection': 'keep-alive',
    'server': 'japronto',
}

POST_HEADERS = {
    'connection': 'close',
    'server': 'japronto',
}


def _validate_entity_id(entity_id):
    try:
        return int(entity_id)
    except ValueError:
        raise ValidationError('Error on parsing entity id - {}'.format(entity_id))


def get_entity(schema, entity_id):
    model = schema.Meta.model
    entity_id = _validate_entity_id(entity_id)
    session = Session()
    entity = session.query(model).get(entity_id)
    if not entity:
        raise EntityDoesNotExist('Entity does not exist')
    return schema().dump(entity).data


def get_entity_or_404(schema):
    def api_func(request):
        try:
            entity_id = request.match_dict.get('entity_id')
            entity = get_entity(schema=schema, entity_id=entity_id)
            if entity:
                return request.Response(json=entity, code=200, headers=GET_HEADERS)
            else:
                return request.Response(code=404, headers=GET_HEADERS)
        except Exception as e:
            logger.error(e)
            return request.Response(code=404, headers=GET_HEADERS)

    return api_func


def update_entity_or_400_or_404(schema):
    def api_func(request):
        try:
            entity_id = request.match_dict.get('entity_id')
            entity = get_entity(schema=schema, entity_id=entity_id)
            if entity:
                parsed = request.json
                if not parsed:
                    raise ValidationError('Empty request body')
                parsed['id'] = entity_id
                session = Session()
                data, errors = schema().load(parsed, session=session)
                if errors:
                    raise ValidationError('invalid request body: {}'.format(errors))
                session.add(data)
                session.commit()
                return request.Response(text='{}', code=200, headers=POST_HEADERS)
            else:
                return request.Response(code=404, headers=POST_HEADERS)
        except (ValidationError, IntegrityError) as e:
            logger.error(e)
            return request.Response(code=400, headers=POST_HEADERS)
        except (ValueError, EntityDoesNotExist) as e:
            logger.error(e)
            return request.Response(code=404, headers=POST_HEADERS)
        except JSONDecodeError as e:
            logger.error(e)
            return request.Response(code=400, headers=POST_HEADERS)

    return api_func


def create_entity_or_400(schema):
    def api_func(request):
        try:
            parsed = request.json
            if not parsed:
                raise ValidationError('Empty request body')
            session = Session()
            data, errors = schema().load(parsed, session=session)
            if errors:
                raise ValidationError('invalid request body: {}'.format(errors))
            entity_id = parsed.get('id', None)
            if not entity_id:
                raise ValidationError('No entity id')
            try:
                get_entity(schema=schema, entity_id=entity_id)
                return request.Response(code=400, headers=POST_HEADERS)
            except EntityDoesNotExist:
                session.add(data)
                session.commit()
                return request.Response(json={}, code=200, headers=POST_HEADERS)
        except (ValidationError, IntegrityError) as e:
            logger.error(e)
            return request.Response(code=400, headers=POST_HEADERS)
        except JSONDecodeError as e:
            logger.error(e)
            return request.Response(code=400, headers=POST_HEADERS)

    return api_func

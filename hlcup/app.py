# -*- coding: utf-8 -*-
# Owner: Bulat <bulat.kurbangaliev@cinarra.com>
import logging

from japronto import Application

from hlcup.api.helpers import get_entity_or_404, update_entity_or_400_or_404, create_entity_or_400
from hlcup.api.locations import location_avg_api
from hlcup.api.users import users_visits_api
from hlcup.schemas import UserSchema, LocationSchema, VisitSchema
from hlcup.settings import MEMORY_BASED, DUMMY_API, JAPRONTO_PORT, WORKER_NUM, JAPRONTO_HOST
from hlcup.load_util import load_data

logger = logging.getLogger(__name__)

if not DUMMY_API and MEMORY_BASED:
    try:
        load_data()
    except Exception as e:
        logger.error('ERROR on load data: {}'.format(e))

app = Application()


def dummy_api(request):
    return request.Response(text='dummy api')


if not DUMMY_API:
    app.router.add_route('/users/new', create_entity_or_400(UserSchema), 'POST')
    app.router.add_route('/users/{entity_id}', get_entity_or_404(UserSchema), 'GET')
    app.router.add_route('/users/{entity_id}', update_entity_or_400_or_404(UserSchema), 'POST')
    app.router.add_route('/users/{entity_id}/visits', users_visits_api, 'GET')

    app.router.add_route('/visits/new', create_entity_or_400(VisitSchema), 'POST')
    app.router.add_route('/visits/{entity_id}', get_entity_or_404(VisitSchema), 'GET')
    app.router.add_route('/visits/{entity_id}', update_entity_or_400_or_404(VisitSchema), 'POST')

    app.router.add_route('/locations/new', create_entity_or_400(LocationSchema), 'POST')
    app.router.add_route('/locations/{entity_id}', get_entity_or_404(LocationSchema), 'GET')
    app.router.add_route('/locations/{entity_id}', update_entity_or_400_or_404(LocationSchema), 'POST')
    app.router.add_route('/locations/{entity_id}/avg', location_avg_api, 'GET')
else:
    app.router.add_route('/users/new', dummy_api, 'POST')
    app.router.add_route('/users/{entity_id}', dummy_api, 'GET')
    app.router.add_route('/users/{entity_id}/visits', dummy_api, 'GET')
    app.router.add_route('/visits/{entity_id}', dummy_api, 'GET')
    app.router.add_route('/visits/new', dummy_api, 'POST')
    app.router.add_route('/locations/new', dummy_api, 'POST')
    app.router.add_route('/locations/{entity_id}', dummy_api, 'GET')
    app.router.add_route('/locations/{entity_id}/avg', dummy_api, 'GET')

app.run(debug=True, port=JAPRONTO_PORT, worker_num=WORKER_NUM, host=JAPRONTO_HOST)

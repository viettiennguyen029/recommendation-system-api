from flask import request
from flask_restx import Resource

from ..util.dto import SettingsDto
from ..service.settings_service import save_settings, get_settings, \
    delete_settings, update_settings

api = SettingsDto.api
_settings = SettingsDto.settings


@api.route('/')
class Settings(Resource):
    @api.expect(_settings, validate=True)
    def post(self):
        data = request.json
        return save_settings(data)


@api.route('/<id>')
class Setting(Resource):
    @api.doc('Get these settings with the given id')
    def get(self, id):
        return get_settings(id)

    @api.doc('Update these settings with the given id')
    @api.expect(_settings, validate=True)
    def put(self, id):
        data = request.json
        return update_settings(id, data)

    def delete(self, id):
        return delete_settings(id)

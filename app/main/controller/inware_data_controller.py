from flask import request
from flask_restx import Resource

from ..util.dto import InwareDataDto
from..service.inware_data_service import save_inware_list_data, \
    get_inware_list_data, get_all_inware_list_data_with_paginations,\
    update_inware_list_data, delete_inware_list_data, get_all_inware_list_data

api = InwareDataDto.api
_inware_data = InwareDataDto.inware_data


@api.route('/')
class InwaresData(Resource):
    def get(self):
        args = request.args
        return get_all_inware_list_data_with_paginations(args)

    def post(self):
        data = request.json
        return save_inware_list_data(data)


@api.route('/all')
class AllInwaresData(Resource):
    def get(self):
        return get_all_inware_list_data()


@api.route('/<id>')
class InwareData(Resource):
    def get(self, id):
        """Get inware list data with a given id"""
        return get_inware_list_data(id)

    def put(self, id):
        data = request.json
        return update_inware_list_data(id, data)

    def delete(self, id):
        return delete_inware_list_data(id)

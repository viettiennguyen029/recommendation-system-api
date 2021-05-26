from flask import request
from flask_restx import Resource

from ..util.dto import InwareListDto
from ..service.inware_list_service import save_inware_list, \
    update_inware_list, delete_inware_list, \
    get_all_inware_lists_with_pagination, get_inware_list

api = InwareListDto.api
_inware_list = InwareListDto.inware_list


@api.route('/')
class InwareLists(Resource):
    @api.doc('List all inware_lists with pagination')
    def get(self):
        args = request.args
        return get_all_inware_lists_with_pagination(args)

    @api.expect(_inware_list, validate=True)
    @api.response(201, 'New inware_list successfully created.')
    @api.doc('Create a new inware_list')
    def post(self):
        """Create a new inware_list """
        data = request.json
        return save_inware_list(data)


@api.route('/<id>')
@api.param('id', 'The inware_list identifier')
class InwareList(Resource):
    @api.doc('Get a inware_list with the given id')
    def get(self, id):
        """Get a inware_list with a given id"""
        return get_inware_list(id)

    @api.doc('Update a inware_list with a given id')
    @api.expect(_inware_list, validate=True)
    def put(self, id):
        """Update a inware_list with a given id"""
        data = request.json
        return update_inware_list(id, data)

    @api.doc('Delete a inware_list with a given id')
    def delete(self, id):
        """Delete a inware_list"""
        return delete_inware_list(id)

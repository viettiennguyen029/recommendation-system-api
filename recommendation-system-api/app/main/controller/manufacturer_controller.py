from flask import request
from flask_restx import Resource

from ..util.dto import ManufacturerDto
from ..service.manufacturer_service import save_manufacturer, \
    update_manufacturer, get_all_manufacturers, get_manufacturer, \
    delete_manufacturer, get_all_manufacturers_with_pagination

api = ManufacturerDto.api
_manufacturer = ManufacturerDto.manufacturer


@api.route('/')
class Manufacturers(Resource):
    @api.doc('List all manufacturers with pagination')
    def get(self):
        args = request.args
        return get_all_manufacturers_with_pagination(args)

    @api.expect(_manufacturer, validate=True)
    @api.response(201, 'New manufacturer successfully created.')
    @api.doc('Create a new manufacturer')
    def post(self):
        """Create a new manufacturer """
        data = request.json
        return save_manufacturer(data)


@api.route('/all')
class ManufacturerList(Resource):
    @api.doc('List all manufacturers')
    def get(self):
        """List all manufacturers in the system"""
        return get_all_manufacturers()


@api.route('/<id>')
@api.param('id', 'The manufacturer identifier')
class manufacturer(Resource):
    @api.doc('Get a manufacturer with the given id')
    def get(self, id):
        """Get a manufacturer with a given id"""
        return get_manufacturer(id)

    @api.doc('Update a manufacturer with a given id')
    @api.expect(_manufacturer, validate=True)
    def put(self, id):
        """Update a manufacturer with a given id"""
        data = request.json
        return update_manufacturer(id, data)

    @api.doc('Delete a manufacturer with a given id')
    def delete(self, id):
        """Delete a manufacturer"""
        return delete_manufacturer(id)

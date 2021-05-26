from flask import request
from flask_restx import Resource

from ..util.dto import UnitDto
from ..service.unit_service import save_unit, get_all_units,\
     get_unit, get_all_units_with_pagination, delete_unit, update_unit

api = UnitDto.api
_unit = UnitDto.unit


@api.route('/')
class Units(Resource):
    def get(self):
        """List all units in the system with pagination filtered"""
        args = request.args
        return get_all_units_with_pagination(args)

    @api.expect(_unit, validate=True)
    @api.response(201, 'Unit successfully created.')
    @api.doc('Create a new unit')
    def post(self):
        """Create a new unit """
        data = request.json
        args = request.args
        return save_unit(data, args)


@api.route('/all')
class UnitList(Resource):
    @api.doc('List all units')
    def get(self):
        """List all units in the system"""
        args = request.args
        return get_all_units(args)


@api.route('/<id>')
@api.param('id', 'The unit identifier')
class Unit(Resource):
    @api.doc('Get a unit with the given id')
    def get(self, id):
        """Get a unit with a given id"""
        args = request.args
        return get_unit(id, args)

    @api.doc('Update a unit with a given id')
    @api.expect(_unit, validate=True)
    def put(self, id):
        """Update a unit with a given id"""
        data = request.json
        args = request.args
        return update_unit(id, data, args)

    @api.doc('Delete a unit with a given id')
    def delete(self, id):
        """Delete a unit"""
        return delete_unit(id, args)

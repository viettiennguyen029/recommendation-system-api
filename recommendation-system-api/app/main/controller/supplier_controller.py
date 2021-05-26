from flask import request
from flask_restx import Resource

from ..util.dto import SupplierDto
from ..service.supplier_service import save_supplier,\
    update_supplier, get_all_suppliers, get_supplier, \
    delete_supplier, get_all_suppliers_with_pagination

api = SupplierDto.api
_supplier = SupplierDto.supplier


@api.route('/')
class Suppliers(Resource):
    @api.doc('List all suppliers with pagination')
    def get(self):
        """List all suppliers in the system"""
        args = request.args
        return get_all_suppliers_with_pagination(args)

    @api.expect(_supplier, validate=True)
    @api.response(201, 'New supplier successfully created.')
    @api.doc('Create a new supplier')
    def post(self):
        """Create a new supplier """
        data = request.json
        return save_supplier(data)


@api.route('/all')
class SupplierList(Resource):
    @api.doc('List all suppliers')
    def get(self):
        """List all suppliers in the system"""
        return get_all_suppliers()


@api.route('/<id>')
@api.param('id', 'The supplier identifier')
class supplier(Resource):
    @api.doc('Get a supplier with the given id')
    def get(self, id):
        """Get a supplier with a given id"""
        return get_supplier(id)

    @api.doc('Update a supplier with a given id')
    @api.expect(_supplier, validate=True)
    def put(self, id):
        """Update a supplier with a given id"""
        data = request.json
        return update_supplier(id, data)

    @api.doc('Delete a supplier with a given id')
    def delete(self, id):
        """Delete a supplier"""
        return delete_supplier(id)

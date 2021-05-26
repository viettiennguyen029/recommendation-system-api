from flask import request
from flask_restx import Resource

from ..util.dto import OtherFeeDto
from ..service.other_fees_service import save_other_fees, \
    update_other_fees, get_all_other_fees_with_pagination, \
    delete_other_fees, get_other_fees

api = OtherFeeDto.api
_other_fee = OtherFeeDto.other_fee


@api.route('/')
class OtherFeeList(Resource):
    @api.doc('List all other fees with pagination')
    def get(self):
        """List all other fees in the system with pagination"""
        args = request.args
        return get_all_other_fees_with_pagination(args)

    @api.expect(_other_fee, validate=True)
    @api.doc('Create a new other fee')
    def post(self):
        """Create a new other fees """
        data = request.json
        return save_other_fees(data)


@api.route('/<id>')
@api.param('id', 'The other fee identifier')
class OtherFee(Resource):
    @api.doc('Get an other fee in a specific time with the given id')
    def get(self, id):
        """Get an other fee with a given id"""
        return get_other_fees(id)

    @api.doc('Update an other fee with a given id')
    @api.expect(_other_fee, validate=True)
    def put(self, id):
        """Update a other fee with a given id"""
        data = request.json
        return update_other_fees(id, data)

    @api.doc('Delete a other_fee with a given id')
    def delete(self, id):
        """Delete a other_fee"""
        return delete_other_fees(id)

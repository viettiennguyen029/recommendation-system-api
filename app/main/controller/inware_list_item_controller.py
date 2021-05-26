from flask import request
from flask_restx import Resource

from ..util.dto import InwareListItemDto
from ..service.inware_list_item_service import save_inware_list_item, \
    get_inware_item, delete_inware_item

api = InwareListItemDto.api
_inware_list_item = InwareListItemDto.inware_list_item


@api.route('/')
class InwareListItems(Resource):
    # @api.doc('List all transactions with pagination')
    # def get(self):
    #     """List all transactions with pagination"""
    #     args = request.args
    #     return get_all_transaction_with_pagination(args)

    @api.expect(_inware_list_item, validate=True)
    @api.doc('Create a new inware item')
    def post(self):
        ''' Create a new inware item '''
        data = request.json
        return save_inware_list_item(data)


@api.route('/<id>')
@api.param('id', 'The inware item identifier')
class InwareListItem(Resource):
    def get(self, id):
        """Get inware item data with a given id"""
        return get_inware_item(id)

    def delete(self, id):
        '''Delete inware item with its related fields'''
        return delete_inware_item(id)

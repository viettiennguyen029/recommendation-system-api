from flask import request
from flask_restx import Resource

from ..util.dto import TransactionListDataDto
from ..service.transaction_list_data_service import save_transaction_list_data, \
    get_transaction_list_data, get_all_transaction_lists_with_pagination, \
    get_all_transaction_list_data, update_transaction_list_data, \
    delete_transaction_list_data, get_all_products_lastest_price

api = TransactionListDataDto.api
_transaction_list_data = TransactionListDataDto.transaction_list_data


@api.route('/')
class TransactionListsData(Resource):
    def post(self):
        data = request.json
        return save_transaction_list_data(data)

    def get(self):
        args = request.args
        return get_all_transaction_lists_with_pagination(args)


@api.route('/all')
class AllTransactionLists(Resource):
    def get(self):
        return get_all_transaction_list_data()


@api.route('/latest-price')
class ProductLatestPrice(Resource):
    def get(self):
        return get_all_products_lastest_price()


@api.route('/<id>')
class TransactionListData(Resource):
    def get(self, id):
        """Get invoice data with a given id"""
        return get_transaction_list_data(id)

    def put(self, id):
        data = request.json
        return update_transaction_list_data(id, data)

    def delete(self, id):
        return delete_transaction_list_data(id)

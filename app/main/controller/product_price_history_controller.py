from flask import request
from flask_restx import Resource

from ..util.dto import ProductPriceHistoryDto
from ..service.product_price_history_service import \
    save_product_price_history, update_product_price_history,\
    delete_product_price_history, get_all_product_price_history,\
    get_product_price_history, get_product_price_history_with_pagination

api = ProductPriceHistoryDto.api
_product_price_history = ProductPriceHistoryDto.product_price_history


@api.route('/')
class ProductPricesHistory(Resource):
    @api.doc('List all product price with pagination')
    def get(self):
        """List all product price with pagination"""
        args = request.args
        return get_product_price_history_with_pagination(args)

    @api.expect(_product_price_history, validate=True)
    @api.doc('Create a new product price history')
    def post(self):
        """Create a new product price history """
        data = request.json
        return save_product_price_history(data)


@api.route('/all')
class ProductPriceHistoryList(Resource):
    @api.doc('List all product price in the system')
    def get(self):
        """List all product price in the system"""
        return get_all_product_price_history()


@api.route('/<id>')
@api.param('id', 'The product price history identifier')
class ProductPriceHistory(Resource):
    @api.doc('Get a product price history')
    def get(self, id):
        """Get a product price history with a given id"""
        return get_product_price_history(id)

    @api.doc('Update a product price history with a given id')
    @api.expect(_product_price_history, validate=True)
    def put(self, id):
        """Update a product price history with a given id"""
        data = request.json
        return update_product_price_history(id, data)

    @api.doc('Delete a product price history with a given id')
    def delete(self, id):
        """Delete a product price history with a given id"""
        return delete_product_price_history(id)

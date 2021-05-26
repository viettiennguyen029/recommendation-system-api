from flask import request
from flask_restx import Resource

from ..util.dto import ProducDataDto
from ..service.product_data_service import get_product_data, \
    save_product_data, get_all_products_with_pagination, \
    delete_product_data, update_product_data, \
    get_all_product_data, upload_image

import werkzeug
import parser
import os

api = ProducDataDto.api
_product_data = ProducDataDto.product_data

parser = api.parser()
parser.add_argument(
    'in_file', type=werkzeug.datastructures.FileStorage,
    location='files')


@api.route('/')
class ProductsData(Resource):
    @api.doc('List all product and price with pagination')
    def get(self):
        """List all product price with pagination"""
        args = request.args
        return get_all_products_with_pagination(args)

    # @api.expect(_product_data, validate=True)
    @api.doc('Create a new product data')
    def post(self):
        """Create a new product data"""
        data = request.json
        return save_product_data(data)


@api.route('/upload-image', methods=['POST'])
class ImageUploader(Resource):
    @api.doc('Handling upload product image')
    @api.expect(parser)
    def post(self):
        image = request.files['in_file']
        return upload_image(image)


@api.route('/all')
class AllProducData(Resource):
    @api.doc('List all product and price without pagination')
    def get(self):
        """List all product and price without pagination"""
        return get_all_product_data()


@api.route('/<id>')
@api.param('id', 'The product data identifier')
class ProductData(Resource):
    def get(self, id):
        """Get product data with a given id"""
        return get_product_data(id)

    @api.doc('Update a product data with a given id')
    # @api.expect(_product_data, validate=True)
    def put(self, id):
        """Update a product data with a given id"""
        data = request.json
        return update_product_data(id, data)

    def delete(self, id):
        '''Delete product with its related fields'''
        return delete_product_data(id)

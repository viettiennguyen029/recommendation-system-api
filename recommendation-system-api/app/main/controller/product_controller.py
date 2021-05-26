from flask import request
from flask import send_from_directory
from flask_restx import Resource

from ..util.dto import ProductDto
from ..service.product_service import save_product,\
    get_all_products, get_product, delete_product,\
    update_product, get_all_products_with_pagination,\
    download_csv, upload_csv, upload_image, upload_image_with_base64


import werkzeug
import parser
import os

api = ProductDto.api
_product = ProductDto.product

parser = api.parser()
# parser.add_argument('param', type=int, help='Some param', location='form')
parser.add_argument(
    'in_files', type=werkzeug.datastructures.FileStorage, location='files')


@api.route('/upload_csv', methods=['POST'])
class WithParserResource(Resource):
    @api.expect(parser)
    def post(self):
        data = request.files['in_files']
        return upload_csv(data)


@api.route('/upload_image', methods=['POST'])
class ImageUpload(Resource):
    @api.doc('Upload product image')
    @api.expect(parser)
    def post(self):
        # content_length = request.content_length
        image = request.files['in_files']
        return upload_image(image)


@api.route('/base64', methods=['POST'])
class HandlingBase64(Resource):
    def post(self):
        data = request.json
        base64_string = data['product_image']
        return upload_image_with_base64(base64_string)


@api.route('/all')
class ProductList(Resource):
    @api.doc('List all products')
    def get(self):
        """List all products"""
        return get_all_products()


@api.route('/')
class Products(Resource):
    @api.doc('List all products with pagination')
    def get(self):
        """List all products with pagination"""
        args = request.args
        return get_all_products_with_pagination(args)

    @api.expect(_product, validate=True)
    @api.doc('Create a new product')
    def post(self):
        """Create a new product """
        data = request.json
        return save_product(data=data)


@api.route('/download_csv', methods=['GET'])
class ExportCSV(Resource):
    @api.doc('Export data into csv file')
    def get(self):
        return download_csv()


@api.route('/<id>')
@api.param('id', 'The product identifier')
class Product(Resource):
    @api.doc('Get a product')
    def get(self, id):
        """Get a product with a given id"""
        return get_product(id)

    @api.doc('Update a product with the given id')
    @api.expect(_product, validate=True)
    def put(self, id):
        data = request.json
        return update_product(id, data)

    @api.doc('Delete a product with a given id')
    def delete(self, id):
        """Delete a product"""
        return delete_product(id)

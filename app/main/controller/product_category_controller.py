from flask import request
from flask_restx import Resource

from ..util.dto import ProductCategoryDto
from ..service.product_category_service import save_product_category,\
    get_product_category, get_all_product_categories,\
    delete_product_category, update_product_category,\
    get_all_product_category_with_pagination

api = ProductCategoryDto.api
_product_category = ProductCategoryDto.product_category


@api.route('/')
class ProductCategories(Resource):
    def get(self):
        """List all product categories with filtered pagination"""
        args = request.args
        return get_all_product_category_with_pagination(args)

    @api.expect(_product_category, validate=True)
    @api.response(201, 'Product category successfully created.')
    @api.doc('Create a new product category')
    def post(self):
        """Create a new product category """
        data = request.json
        return save_product_category(data=data)


@api.route('/all')
class ProductCategoryList(Resource):
    @api.doc('List all product categories')
    def get(self):
        """List all product categories"""
        return get_all_product_categories()


@api.route('/<id>')
@api.param('id', 'The product category identifier')
class ProductCategory(Resource):
    @api.doc('Get a product category')
    def get(self, id):
        """Get a product category with a given id"""
        return get_product_category(id)

    @api.doc('Update a product category with a given id')
    @api.expect(_product_category, validate=True)
    def put(self, id):
        """Update a product category with a given id"""
        data = request.json
        return update_product_category(id, data)

    @api.doc('Delete a product category with a given id')
    def delete(self, id):
        """Delete a product category"""
        return delete_product_category(id)

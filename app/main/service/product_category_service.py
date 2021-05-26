import datetime
import math

from sqlalchemy import desc, asc

from app.main import db
from app.main.model.product_category import ProductCategory


def save_product_category(data):
    errors = {}

    # Check unique field is null or not
    if data['name'] == "":
        errors['name'] = ['Product category name must not be null!']
    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new product category!',
            'errors': errors
        }
        return response_object, 200
    else:
        product_category = ProductCategory.query.filter_by(
            name=data['name']).first()

        if product_category:
            errors['name'] = ['Product category name is already existed!']
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a new product_category!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_product_category = ProductCategory(
                name=data['name'],
                description=data['description'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            save_changes(new_product_category)

            output = {}
            output['name'] = new_product_category.name
            output['description'] = new_product_category.description
            output['created_on'] = str(new_product_category.created_on)
            output['updated_on'] = str(new_product_category.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new product category is created successfully!',
                'data': output
            }
            return response_object, 201


def update_product_category(id, data):
    product_category = ProductCategory.query.filter_by(id=id).first()
    is_updated = False
    errors = {}

    # Check if ID is valid or not
    if not product_category:
        errors['id'] = ["Product category ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not update product category's information!",
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == "":
            errors['name'] = ["Product category name must not be null!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update product category's information!",
                'errors': errors
            }
            return response_object, 200
        else:
            if data['name'] != product_category.name:
                # Check if product_category name is existed or not
                updated_product_category = product_category.query.filter_by(
                    name=data['name']).first()
                if updated_product_category:
                    errors['name'] = [
                        "Product category name is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update product category's information!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    product_category.name = data['name']

            if data['description'] != product_category.description:
                is_updated = True
                product_category.description = data['description']

            if is_updated is True:
                product_category.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            product_category_data = {}
            product_category_data['name'] = product_category.name
            product_category_data['description'] = product_category.description
            product_category_data['created_on'] = str(
                product_category.created_on)
            product_category_data['updated_on'] = str(
                product_category.updated_on)

            respone_object = {
                'status': 'SUCCESS',
                'message': 'Successfully updated product_category information!',
                'data': product_category_data
            }
            return respone_object, 200


def get_all_product_categories():
    all_product_category = ProductCategory.query.all()
    output = []

    for product_category in all_product_category:
        product_category_data = {}
        product_category_data['id'] = str(product_category.id)
        product_category_data['name'] = product_category.name
        product_category_data['description'] = product_category.description
        product_category_data['created_on'] = str(product_category.created_on)
        product_category_data['updated_on'] = str(product_category.updated_on)

        output.append(product_category_data)

    data = {}
    data['product_categories'] = output

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all product categories',
        'data': data
    }
    return respone_object, 200


def get_product_category(id):
    errors = {}
    product_category = ProductCategory.query.filter_by(id=id).first()

    if not product_category:
        errors['id'] = ['Product category ID does not exist!']
        respone_object = {
            'status': 'FAILED',
            'message': "Can not get product category's information!",
            'errors': errors
        }
        return respone_object, 200

    product_category_data = {}
    product_category_data['id'] = product_category.id
    product_category_data['name'] = product_category.name
    product_category_data['description'] = product_category.description
    product_category_data['created_on'] = str(product_category.created_on)
    product_category_data['updated_on'] = str(product_category.updated_on)

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of product category',
        'data': product_category_data
    }
    return respone_object, 200


def delete_product_category(id):
    errors = {}
    product_category = ProductCategory.query.filter_by(id=id).first()

    if not product_category:
        errors['id'] = ['Product category ID does not exist!']
        respone_object = {
            'status': 'FAILED',
            'message': "Can not delete product category",
            'errors': errors
        }
        return respone_object, 200
    else:
        db.session.delete(product_category)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted product category!'
        }
        return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def get_all_product_category_with_pagination(args):
    # Query Params
    page_size = 10
    current_page = 1
    next_page = False
    key_word = None
    sort_field = None
    sort_order = -1

    # Check query param value
    if "page_size" in args:
        page_size = int(args['page_size'])
    if "current_page" in args:
        current_page = int(args['current_page'])
    if "key_word" in args:
        key_word = args['key_word']
    if "sort_field" in args:
        sort_field = args['sort_field']
    if "sort_order" in args:
        sort_order = int(args['sort_order'])

    # Sort by order value
    if sort_field is None or sort_order is None:
        '''Default order by the lasted created_on value'''
        product_category = ProductCategory.query.order_by(
            ProductCategory.created_on.desc())
    else:
        if sort_order == -1:
            product_category = ProductCategory.query.order_by(
                desc(sort_field))
        else:
            product_category = ProductCategory.query.order_by(
                asc(sort_field))

    product_category_on_page = product_category.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(product_category.count() / page_size)

    if math.ceil(product_category.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for product_cat in product_category_on_page:
        # Sort by keyword
        if (key_word is not None):
            if (key_word in product_cat.name.lower()) or (
                    key_word in product_cat.description.lower()):
                product_category_data = {}
                product_category_data['id'] = product_cat.id
                product_category_data['name'] = product_cat.name
                product_category_data['description'] = product_cat.description
                product_category_data['created_on'] = str(
                    product_cat.created_on)
                product_category_data['updated_on'] = str(
                    product_cat.updated_on)

                output.append(product_category_data)
        else:
            product_category_data = {}
            product_category_data['id'] = product_cat.id
            product_category_data['name'] = product_cat.name
            product_category_data['description'] = product_cat.description
            product_category_data['created_on'] = str(product_cat.created_on)
            product_category_data['updated_on'] = str(product_cat.updated_on)

            output.append(product_category_data)

    data = {}
    data['product_categories'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all product category',
        'data': data
    }
    return response_object, 200

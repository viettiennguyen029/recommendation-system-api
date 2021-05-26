import datetime
import math

from sqlalchemy import desc, asc
from app.main import db
from app.main.model.product_price_history import ProductPriceHistory
from app.main.model.product import Product


def save_product_price_history(data):
    errors = {}

    # Check null
    if data['effective_date'] == "":
        errors['effective_date'] = ['Price updated date must not be null!']

    if data['original_price'] == "":
        errors['original_price'] = ['Product original price must not be null!']

    if data['sale_price'] == "":
        errors['sale_price'] = ['Product sale price must not be null!']

    if data['product_id'] == "":
        errors['product_id'] = ['Product ID must not be null!']

    # Check type
    if data['original_price'].isnumeric() is False:
        errors['original_price'] = ['Product original price is not valid!']

    if data['sale_price'].isnumeric() is False:
        errors['sale_price'] = ['Product sale price is not valid!']

    if data['product_id'].isnumeric() is False:
        errors['product_id'] = ['Product ID is not valid!']

    # Check if foregin key is valid or not
    product = Product.query.filter_by(id=data['product_id']).first()
    if not product:
        errors['product_id'] = ['Product ID does not exist']

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new product price history!',
            'errors': errors
        }
        return response_object, 200
    else:
        # effective date and product_id cannot be the same at once record
        product_price = ProductPriceHistory.query.filter_by(
            product_id=data['product_id'],
            effective_date=data['effective_date']).first()

        if product_price:
            errors['product price'] = 'Product price is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a new product price history!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_price_history = ProductPriceHistory(
                original_price=data['original_price'],
                sale_price=data['sale_price'],
                effective_date=datetime.datetime.strptime(
                    data['effective_date'], '%Y-%m-%d'),
                product_id=data['product_id'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            db.session.add(new_price_history)
            db.session.commit()

            output = {}
            output['id'] = str(new_price_history.id)
            output['original_price'] = str(new_price_history.original_price)
            output['sale_price'] = str(new_price_history.sale_price)
            output['effective_date'] = str(
                new_price_history.effective_date)
            output['product_id'] = str(new_price_history.product_id)
            output['created_on'] = str(new_price_history.created_on)
            output['updated_on'] = str(new_price_history.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new product price history is created successfully!',
                'data': output
            }
            return response_object, 201


def get_all_product_price_history():
    all_price_history = ProductPriceHistory.query.all()
    output = []

    for price_history in all_price_history:
        price_history_data = {}
        price_history_data['id'] = str(price_history.id)
        price_history_data['original_price'] = str(
            price_history.original_price)
        price_history_data['sale_price'] = str(price_history.sale_price)
        price_history_data['effective_date'] = str(
            price_history.effective_date)
        price_history_data['product_id'] = str(price_history.product_id)
        price_history_data['created_on'] = str(price_history.created_on)
        price_history_data['updated_on'] = str(price_history.updated_on)

        output.append(price_history_data)

    data = {}
    data['product_price_history'] = output

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all product price!',
        'data': data
    }

    return respone_object, 200


def get_product_price_history(id):
    errors = {}
    product_price_history = ProductPriceHistory.query.filter_by(id=id).first()

    if not product_price_history:
        errors['ID'] = ['Product Price History does not exist']
        response_object = {
            'status': 'FAILED',
            'message': 'Fail to get product price history',
            'errors': errors
        }
        return response_object, 200

    price_history_data = {}
    price_history_data['id'] = str(
        product_price_history.id)
    price_history_data['original_price'] = str(
        product_price_history.original_price)
    price_history_data['sale_price'] = str(
        product_price_history.sale_price)
    price_history_data['effective_date'] = str(
        product_price_history.effective_date)
    price_history_data['product_id'] = str(
        product_price_history.product_id)
    price_history_data['created_on'] = str(
        product_price_history.created_on)
    price_history_data['updated_on'] = str(
        product_price_history.updated_on)

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of product price history!',
        'data': price_history_data
    }

    return response_object, 200


def delete_product_price_history(id):
    product_price_history = ProductPriceHistory.query.filter_by(
        id=id).first()

    if not product_price_history:
        respone_object = {
            'status': 'ERROR',
            'message': 'Product price history does not exist!'
        }
        return respone_object, 200
    else:
        db.session.delete(product_price_history)
        db.session.commit()

    response_object = {
        'status': 'SUCCESS',
        'message': 'Successfully deleted the product log!'
    }
    return response_object, 200


def update_product_price_history(id, data):
    product_price_history = ProductPriceHistory.query.filter_by(id=id).first()
    is_updated = False
    errors = {}

    if not product_price_history:
        errors['id'] = ["Product price history ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': 'Cannot get Product price history!',
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['product_id'] == "":
            errors['product_id'] = ['Product ID must not be null!']

        if data['original_price'] == "":
            errors['original_price'] = [
                'Product original price must not be null!']

        if data['sale_price'] == "":
            errors['sale_price'] = ['Product sale price must not be null!']

        if data['effective_date'] == "":
            errors['effective_date'] = [
                'Price effective date must not be null!']

        # Check if foregin key is valid or not
        product = Product.query.filter_by(id=data['product_id']).first()
        if not product:
            errors['product_id'] = ["Product ID does not exist!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update product price history!",
                'errors': errors
            }
            return response_object, 200
        else:
            # effective date and product_id cannot be the same at once record
            product_price = ProductPriceHistory.query.filter_by(
                product_id=data['product_id'],
                effective_date=data['effective_date']).first()
            if (product_price and
                (product_price.product_id != str(data['product_id']) or
                 product_price.effective_date != datetime.datetime.strptime(
                    data['effective_date'], '%Y-%m-%d'))):
                errors['effective_date'] = [
                    "Effective date and product_id is already existed"]
                response_object = {
                    'status': 'FAILED',
                    'message': "Can not update product price history!",
                    'errors': errors
                }
                return response_object, 200
            else:
                if data['product_id'] != str(product_price.product_id):
                    is_updated = True
                    product_price.product_id = data['product_id']

                if data['original_price'] != product_price.original_price:
                    is_updated = True
                    product_price.original_price = data['original_price']

                if data['sale_price'] != product_price.sale_price:
                    is_updated = True
                    product_price.sale_price = data['sale_price']

                if data['effective_date'] != product_price.effective_date:
                    is_updated = True
                    product_price.effective_date = datetime.datetime.strptime(
                        data['effective_date'], '%Y-%m-%d')

                if is_updated is True:
                    product_price.updated_on = datetime.datetime.utcnow()
                    db.session.commit()

            product_price_data = {}
            product_price_data['id'] = str(product_price.id)
            product_price_data['original_price'] = str(
                product_price.original_price)
            product_price_data['sale_price'] = str(product_price.sale_price)
            product_price_data['effective_date'] = str(
                product_price.effective_date)
            product_price_data['product_id'] = str(product_price.product_id)
            product_price_data['created_on'] = str(product_price.created_on)
            product_price_data['updated_on'] = str(product_price.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated product price history!",
                'data': product_price_data
            }
            return response_object, 200


def get_product_price_history_with_pagination(args):
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
        key_word = args['key_word'].lower()
    if "sort_field" in args:
        sort_field = args['sort_field']
    if "sort_order" in args:
        sort_order = int(args['sort_order'])

    # Sort by order value
    if sort_field is None or sort_order is None:
        '''Default order by the lasted created_on value'''
        product_price_history = ProductPriceHistory.query.order_by(
            ProductPriceHistory.created_on.desc())
    else:
        if sort_order == -1:
            product_price_history = ProductPriceHistory.query.order_by(
                desc(sort_field))
        else:
            product_price_history = ProductPriceHistory.query.order_by(
                asc(sort_field))

    product_price_history_on_page = product_price_history.limit(
        page_size).offset((current_page - 1) * page_size)
    total_pages = math.ceil(product_price_history.count() / page_size)

    if math.ceil(product_price_history.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for product_price in product_price_history_on_page:
        product = Product.query.filter_by(
            id=product_price.product_id).first()
        # Sort by keyword
        if (key_word is not None):
            if (key_word in str(product_price.original_price)) or (
                key_word in str(product_price.sale_price)) or (
                    key_word in product.name.lower()):
                product_price_data = {}
                product_price_data['id'] = str(
                    product_price.id)
                product_price_data['original_price'] = str(
                    product_price.original_price)
                product_price_data['sale_price'] = str(
                    product_price.sale_price)
                product_price_data['effective_date'] = str(
                    product_price.effective_date)
                product_price_data['product'] = {}
                product_price_data['product']['id'] = str(
                    product.id)
                product_price_data['product']['name'] = str(
                    product.name)

                output.append(product_price_data)
        else:
            product_price_data = {}
            product_price_data['id'] = str(
                product_price.id)
            product_price_data['original_price'] = str(
                product_price.original_price)
            product_price_data['sale_price'] = str(
                product_price.sale_price)
            product_price_data['effective_date'] = str(
                product_price.effective_date)
            product_price_data['product'] = {}
            product_price_data['product']['id'] = str(
                product.id)
            product_price_data['product']['name'] = product.name

            output.append(product_price_data)

    data = {}
    data['products_price_history'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully getting information of all products price history',
        'data': data
    }
    return response_object, 200

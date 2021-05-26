import datetime
import math

from app.main import db
from sqlalchemy import desc, asc

from app.main.model.inware_list import InwareList
from app.main.model.product import Product
from app.main.model.inware_list_item import InwareListItem


def save_inware_list_item(data):
    errors = {}

    # Check null
    if data['product_id'] == "":
        errors['product_id'] = ['Product id must not be null!']

    if data['inware_list_id'] == "":
        errors['inware_list_id'] = ['Inware list id must not be null!']

    if data['quantity'] == "":
        errors['quantity'] = ['Quantity must not be null!']

    if data['price'] == "":
        errors['price'] = ['Inware price must not be null!']

    # Check if foregin key is valid or not
    inware_list = InwareList.query.filter_by(
        id=data['inware_list_id']).first()
    if not inware_list:
        errors['inware_list_id'] = ["Inware list ID does not exist!"]

    product = Product.query.filter_by(id=data['product_id']).first()
    if not product:
        errors['product_id'] = ["Product ID does not exist!"]

    # Check type
    if data['quantity'].isnumeric() is False:
        errors['quantity'] = ['Quatity is not valid!']

    if data['price'].isnumeric() is False:
        errors['price'] = ['Inware price is not valid!']

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new inware list item!',
            'errors': errors
        }
        return response_object, 200
    else:
        inware_list_item = InwareListItem.query.filter_by(
            product_id=data['product_id'], inware_list_id=data['inware_list_id']).first()
        if inware_list_item:
            errors['inware_list_id, product_id'] = 'Inware Item is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a new inware item!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_inware_item = InwareListItem(
                product_id=data['product_id'],
                inware_list_id=data['inware_list_id'],
                price=data['price'],
                quantity=data['quantity'],
                amount=int(data['price']) * int(data['quantity']),
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            db.session.add(new_inware_item)
            db.session.commit()

            output = {}
            output['id'] = str(new_inware_item.id)
            output['inware_list_id'] = str(new_inware_item.inware_list_id)
            output['product_id'] = str(new_inware_item.product_id)
            output['price'] = str(new_inware_item.price)
            output['quantity'] = str(new_inware_item.quantity)
            output['amount'] = str(new_inware_item.amount)
            output['created_on'] = str(new_inware_item.created_on)
            output['updated_on'] = str(new_inware_item.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new inware item is created successfully!',
                'inware-item': output
            }
            return response_object, 201


def get_inware_item(id):
    errors = {}
    inware_item = InwareListItem.query.filter_by(id=id).first()
    if not inware_item:
        errors['id'] = ["Inware item ID does not exist"]
        response_object = {
            'status': 'FAILED',
            'message': 'Can not get inware item data',
            'errors': errors
        }
        return response_object, 200

    product = Product.query.filter_by(
        id=inware_item.product_id).first()
    inware_list = InwareList.query.filter_by(
        id=inware_item.inware_list_id).first()

    inware_item_data = {}
    inware_item_data['id'] = str(inware_item.id)
    inware_item_data['inware_list'] = {}
    inware_item_data['inware_list']['id'] = str(inware_list.id)
    inware_item_data['inware_list']['name'] = str(inware_list.name)
    inware_item_data['product'] = {}
    inware_item_data['product']['id'] = str(product.id)
    inware_item_data['product']['name'] = str(product.name)
    inware_item_data['price'] = str(inware_item.price)
    inware_item_data['quantity'] = str(inware_item.quantity)
    inware_item_data['amount'] = str(inware_item.amount)
    inware_item_data['created_on'] = str(inware_item.created_on)
    inware_item_data['updated_on'] = str(inware_item.updated_on)

    response_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully getting inware item data',
        'data': inware_item_data
    }
    return response_object, 200


def delete_inware_item(id):
    errors = {}
    inware_item = InwareListItem.query.filter_by(id=id).first()
    if not inware_item:
        errors = ['inware_item ID is not valid']
        respone_object = {
            'status': 'ERROR',
            'message': 'Can not delete inware_item!',
            'error:': errors
        }
        return respone_object, 200
    else:
        db.session.delete(inware_item)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted inware item!'
        }
        return response_object, 200


def get_all_inware_item_with_pagination(args):
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
    if "page" in args:
        current_page = int(args['page'])
    if "key_word" in args:
        key_word = args['key_word'].lower()
    if "sort_field" in args:
        sort_field = args['sort_field']
    if "sort_order" in args:
        sort_order = int(args['sort_order'])

    # Sort by order value
    if sort_field is None or sort_order is None:
        '''Default order by the lasted created_on value'''
        inware_items = InwareListItem.query.order_by(
            InwareListItem.created_on.desc())
    else:
        if sort_order == -1:
            inware_items = InwareListItem.query.order_by(desc(sort_field))
        else:
            inware_items = InwareListItem.query.order_by(asc(sort_field))

    inware_items_on_page = inware_items.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(inware_items.count() / page_size)

    if math.ceil(inware_items.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []
    for inware_item in inware_items_on_page:
        product = Product.query.filter_by(
            id=inware_item.product_id).first()
        inware_list = InwareList.query.filter_by(
            id=inware_item.inware_list_id).first()

        # Sort by keyword
        if (key_word is not None):
            if (key_word in str(inware_item.invoice_id)) or (
                    key_word in product.name):
                inware_item_data = {}
                inware_item_data['id'] = str(inware_item.id)
                inware_item_data['invoice'] = {}
                inware_item_data['invoice']['id'] = str(invoice.id)
                inware_item_data['invoice']['invoice_date'] = str(
                    invoice.invoice_date)
                inware_item_data['product'] = {}
                inware_item_data['product']['id'] = str(product.id)
                inware_item_data['product']['name'] = str(product.name)
                '''inware_item_data['product']['value'] = str(product.id)
                inware_item_data['product']['label'] = str(product.name)'''
                inware_item_data['product_price'] = str(
                    inware_item.product_price)
                inware_item_data['effective_date'] = str(
                    product_price_history.effective_date)
                inware_item_data['quantity'] = str(inware_item.quantity)
                inware_item_data['amount'] = str(inware_item.amount)
                inware_item_data['created_on'] = str(inware_item.created_on)
                inware_item_data['updated_on'] = str(inware_item.updated_on)

                output.append(inware_item_data)
        else:
            inware_item_data = {}
            inware_item_data['id'] = str(inware_item.id)
            inware_item_data['invoice'] = {}
            inware_item_data['invoice']['id'] = str(invoice.id)
            inware_item_data['invoice']['invoice_date'] = str(
                invoice.invoice_date)
            inware_item_data['product'] = {}
            inware_item_data['product']['id'] = str(product.id)
            inware_item_data['product']['name'] = str(product.name)
            '''inware_item_data['product']['value'] = str(product.id)
            inware_item_data['product']['label'] = str(product.name)'''
            inware_item_data['product_price'] = str(
                inware_item.product_price)
            inware_item_data['effective_date'] = str(
                product_price_history.effective_date)
            inware_item_data['quantity'] = str(inware_item.quantity)
            inware_item_data['amount'] = str(inware_item.amount)
            inware_item_data['created_on'] = str(inware_item.created_on)
            inware_item_data['updated_on'] = str(inware_item.updated_on)

            output.append(inware_item_data)

    data = {}
    data['inware_items'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all inware_items',
        'data': data
    }
    return response_object, 200

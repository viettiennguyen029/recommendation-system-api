import datetime
import math

from app.main import db
from sqlalchemy import desc, asc

from app.main.model.product import Product
from app.main.model.inware_list import InwareList
from app.main.model.inware_list_item import InwareListItem


def save_inware_list_data(data):
    errors = {}

    # Check null
    if data['name'] == "":
        errors['name'] = ['Inware list name must not be null!']

    if data['record_date'] == "":
        errors['record_date'] = ['Inware list record date must not be null!']

    # inware_items = []
    for inware_item in data['inware_list_items']:
        # Check foregin key - product
        product = Product.query.filter_by(
            id=inware_item['product']['value']).first()
        if not product:
            errors['product'] = ["Product ID does not exist!"]

        # if inware_item['product_id'] in inware_items:
        #     response_object = {
        #         'status': 'FAILED',
        #         'message': 'Product id is duplicated!',
        #         'errors': {}
        #     }
        #     return response_object, 200

    #     inware_items.append(inware_item['product_id'])

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new inware list!',
            'errors': errors
        }
        return response_object, 200
    else:
        new_inware_list = InwareList(
            name=data['name'],
            notes=data['notes'],
            total_amount=0,
            record_date=datetime.datetime.strptime(
                data['record_date'], '%Y-%m-%d'),
            created_on=datetime.datetime.utcnow(),
            updated_on=datetime.datetime.utcnow()
        )
        db.session.add(new_inware_list)
        db.session.commit()

        inware_list_items = {}
        i_total_amount = 0
        for item in data['inware_list_items']:
            new_inware_item = InwareListItem(
                price=item['price'],
                quantity=item['quantity'],
                amount=int(item['price'])*int(item['quantity']),
                inware_list_id=new_inware_list.id,
                product_id=item['product']['value'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            db.session.add(new_inware_item)
            i_total_amount += new_inware_item.amount

        new_inware_list.total_amount = i_total_amount
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'A new inware list is created successfully!'
        }
        return response_object, 201


def get_inware_list_data(id):
    errors = {}
    inware_list = InwareList.query.filter_by(id=id).first()

    if not inware_list:
        errors['id'] = ["Inware list ID does not exist"]
        response_object = {
            'status': 'FAILED',
            'message': 'Can not get inware list data',
            'errors': errors
        }
        return response_object, 200

    inware_list_items = InwareListItem.query.filter_by(
        inware_list_id=id)
    inware_items = {}

    for item in inware_list_items:
        # Query Product
        product = Product.query.filter_by(
            id=item.product_id).first()

        inware_item_key = str(item.id)
        inware_items[inware_item_key] = {}
        inware_items[inware_item_key]['product'] = {}
        inware_items[inware_item_key]['product']['value'] = str(
            product.id)
        inware_items[inware_item_key]['product']['label'] = product.name
        inware_items[inware_item_key]['price'] = str(
            item.price)
        inware_items[inware_item_key]['quantity'] = str(
            item.quantity)
        inware_items[inware_item_key]['total_amount'] = str(
            item.amount)
        inware_items[inware_item_key]['created_on'] = str(
            item.created_on)
        inware_items[inware_item_key]['updated_on'] = str(
            item.updated_on)

    inware_data = {}
    inware_data['id'] = str(inware_list.id)
    inware_data['name'] = inware_list.name
    inware_data['notes'] = inware_list.notes
    inware_data['record_date'] = str(inware_list.record_date).split(' ')[0]
    inware_data['created_on'] = str(inware_list.created_on)
    inware_data['updated_on'] = str(inware_list.updated_on)
    inware_data['total_amount'] = str(inware_list.total_amount)
    inware_data['inware_list_items'] = inware_items

    response_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully getting inware list data',
        'data': inware_data
    }
    return response_object, 200


def get_all_inware_list_data_with_paginations(args):
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
        key_word = args['key_word']
    if "sort_field" in args:
        sort_field = args['sort_field']
    if "sort_order" in args:
        sort_order = int(args['sort_order'])

    # Sort by order value
    if sort_field is None or sort_order is None:
        '''Default order by the lasted created_on value'''
        inware_lists = InwareList.query.order_by(
            InwareList.created_on.desc())
    else:
        if sort_order == -1:
            inware_lists = InwareList.query.order_by(
                desc(sort_field))
        else:
            inware_lists = InwareList.query.order_by(
                asc(sort_field))

    inware_lists_on_page = inware_lists.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(inware_lists.count() / page_size)

    if math.ceil(inware_lists.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for inware_list in inware_lists_on_page:
        # Sort by keyword
        if (key_word is not None):
            if (key_word.lower() in inware_list.name.lower()) or (
                    key_word.lower() in str(inware_list.record_date)):
                inware_list_data = {}
                inware_list_data['id'] = str(inware_list.id)
                inware_list_data['name'] = inware_list.name
                inware_list_data['notes'] = inware_list.notes
                inware_list_data['record_date'] = str(
                    inware_list.record_date).split(' ')[0]
                inware_list_data['total_amount'] = str(
                    inware_list.total_amount)
                inware_list_data['created_on'] = str(inware_list.created_on)
                inware_list_data['updated_on'] = str(inware_list.updated_on)

                output.append(inware_list_data)
        else:
            inware_list_data = {}
            inware_list_data['id'] = str(inware_list.id)
            inware_list_data['name'] = inware_list.name
            inware_list_data['notes'] = inware_list.notes
            inware_list_data['record_date'] = str(
                inware_list.record_date).split(' ')[0]
            inware_list_data['total_amount'] = str(
                inware_list.total_amount)
            inware_list_data['created_on'] = str(inware_list.created_on)
            inware_list_data['updated_on'] = str(inware_list.updated_on)

            output.append(inware_list_data)

    data = {}
    data['inware_lists'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting all inware lists data',
        'data': data
    }
    return response_object, 200


def update_inware_list_data(id, data):
    inware_list = InwareList.query.filter_by(id=id).first()
    inware_items = InwareListItem.query.filter_by(
        inware_list_id=id)
    is_updated = False
    errors = {}

    if not inware_list:
        errors['id'] = ["Inware list ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': 'Cannot update inware list data!',
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == "":
            errors['name'] = ["Inware list name must not be null"]

        if data['record_date'] == "":
            errors['record_date'] = ["Inware list name must not be null"]

        for item in data['inware_list_items']:
            # Check if foregin key "product_id" is valid or not
            product_id = item['product']['value']
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                errors['product_id'] = [
                    "Product id " + product_id + " is not valid"]

            if item['price'] == "":
                errors['price'] = ["Inware item price can not be null"]

            if item['quantity'] == "":
                errors['quantity'] = ["Inware item quantity can not be null"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update inware list data!",
                'errors': errors
            }
            return response_object, 200
        else:
            # Update inware list
            if data['name'] != inware_list.name:
                is_updated = True
                inware_list.name = data['name']

            if data['notes'] != inware_list.notes:
                is_updated = True
                inware_list.notes = data['notes']

            dt_record_date = datetime.datetime.strptime(
                data['record_date'], '%Y-%m-%d')
            if dt_record_date != inware_list.record_date:
                is_updated = True
                inware_list.record_date = dt_record_date

            # For loop to update inware list items
            db_items = []
            request_items = []
            i_total_amount = inware_list.total_amount
            for db_item in inware_items:
                db_items.append(db_item.product_id)

            for item in data['inware_list_items']:
                # Compare product_id in request with others in db
                # If has, compare price and quantiy
                p_id = item['product']['value']
                i_price = int(item["price"])
                i_quantity = int(item["quantity"])

                request_items.append(p_id)

                if p_id in str(db_items):
                    inware_list_item = InwareListItem.query.filter_by(
                        inware_list_id=id, product_id=p_id).first()

                    if (i_price != inware_list_item.price or i_quantity != inware_list_item.quantity):
                        i_total_amount -= inware_list_item.amount
                        inware_list_item.price = i_price
                        inware_list_item.quantity = i_quantity
                        inware_list_item.amount = i_price * i_quantity
                        i_total_amount += inware_list_item.amount
                        is_updated = True
                else:
                    is_updated = True
                    # If does not aldready exist, add new
                    new_inware_item = InwareListItem(
                        inware_list_id=id,
                        product_id=p_id,
                        price=i_price,
                        quantity=i_quantity,
                        amount=i_price*i_quantity,
                        created_on=datetime.datetime.utcnow(),
                        updated_on=datetime.datetime.utcnow()
                    )
                    db.session.add(new_inware_item)
                    i_total_amount += new_inware_item.amount

            for db_item in inware_items:
                # Check if product_id is not exist in request, then delete
                if not (str(db_item.product_id) in request_items):
                    i_total_amount -= db_item.amount
                    db.session.delete(db_item)
                    is_updated = True

            if is_updated is True:
                inware_list.total_amount = i_total_amount
                inware_list.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated inware data",
            }
            return response_object, 200


def delete_inware_list_data(id):
    errors = {}
    # Delete inware items
    inware_list_items = InwareListItem.query.filter_by(
        inware_list_id=id)
    inware_list = InwareList.query.filter_by(
        id=id).first()

    if ((not inware_list) or (not inware_list_items)):
        errors = ['Inware list ID is not valid']
        respone_object = {
            'status': 'ERROR',
            'message': 'Can not delete inware list data!',
            'error:': errors
        }
        return respone_object, 200
    else:
        for item in inware_list_items:
            db.session.delete(item)

        db.session.delete(inware_list)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted inware list data!'
        }
        return response_object, 200


def get_all_inware_list_data():
    all_inware_list_data = InwareList.query.all()
    output = []

    for inware_list in all_inware_list_data:
        inware_list_data = {}
        inware_list_data['id'] = str(inware_list.id)
        inware_list_data['name'] = inware_list.name
        inware_list_data['notes'] = inware_list.notes
        inware_list_data['record_date'] = str(
            inware_list.record_date).split(' ')[0]
        inware_list_data['total_amount'] = str(inware_list.total_amount)
        inware_list_data['created_on'] = str(inware_list.created_on)
        inware_list_data['updated_on'] = str(inware_list.updated_on)

        output.append(inware_list_data)

    data = {}
    data['inware_list'] = output

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all inware lists',
        'data': data
    }
    return respone_object, 200

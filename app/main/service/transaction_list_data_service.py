import datetime
import math

from app.main import db
from sqlalchemy import desc, asc

from app.main.model.product import Product
from app.main.model.transaction_list import TransactionList
from app.main.model.transaction_list_item import TransactionListItem
from app.main.model.product_price_history import ProductPriceHistory


def calc_the_nearest_sale_price(product_id, transaction_list_id):
    transaction_list = TransactionList.query.filter_by(
        id=transaction_list_id).first()

    product_price_history = ProductPriceHistory.query.filter_by(
        product_id=product_id)

    backward_time = []
    for product_price in product_price_history:
        if (product_price.effective_date < transaction_list.transaction_list_date):
            backward_time.append(product_price.effective_date)

    if not backward_time:
        return 0
    else:
        nearest_date = max(backward_time)

        product_nearest_price = ProductPriceHistory.query.filter_by(
            product_id=product_id, effective_date=nearest_date).first()

        return product_nearest_price.sale_price


def save_transaction_list_data(data):
    errors = {}
    # Check null
    if data['customer_id'] == "":
        errors['customer_id'] = ['Customer id must not be null!']

    # if data['total_amount'] == "":
    #     errors['total_amount'] = ['Total amount must not be null!']

    if data['transaction_list_date'] == "":
        errors['transaction_list_date'] = [
            'Transaction date must not be null!']

    # invoice_items = []
    for transaction_list_item in data['transaction_list_items']:
        # Check foregin key - product
        product = Product.query.filter_by(
            id=transaction_list_item['product']['value']).first()
        if not product:
            errors['product'] = ["Product ID does not exist!"]

        # if invoice_item['product_id'] in invoice_items:
        #     response_object = {
        #         'status': 'FAILED',
        #         'message': 'Product id is duplicated!',
        #         'errors': {}
        #     }
        #     return response_object, 200

    #     invoice_items.append(invoice_item['product_id'])

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new inovice',
            'errors': errors
        }
        return response_object, 200
    else:
        new_transaction_list = TransactionList(
            customer_id=data['customer_id'],
            total_amount=0,
            notes=data['note'],
            transaction_list_date=datetime.datetime.strptime(
                data['transaction_list_date'], '%Y-%m-%d'),
            created_on=datetime.datetime.utcnow(),
            updated_on=datetime.datetime.utcnow()
        )
        db.session.add(new_transaction_list)
        db.session.commit()

        transaction_list_items = {}
        i_total_amount = 0
        for item in data['transaction_list_items']:
            product_sale_price = calc_the_nearest_sale_price(
                item['product']['value'], new_transaction_list.id)
            # print(product_sale_price)
            new_transaction_list_item = TransactionListItem(
                transaction_list_id=str(new_transaction_list.id),
                product_id=item['product']['value'],
                product_price=product_sale_price,
                quantity=item['quantity'],
                amount=product_sale_price * int(item['quantity']),
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            db.session.add(new_transaction_list_item)
            i_total_amount += new_transaction_list_item.amount

        new_transaction_list.total_amount = i_total_amount
        db.session.commit()
        response_object = {
            'status': 'SUCCESS',
            'message': 'A new new transaction list is created successfully!'
        }
        return response_object, 201


def get_transaction_list_data(id):
    errors = {}
    transaction_list = TransactionList.query.filter_by(id=id).first()

    if not transaction_list:
        errors['id'] = ["Transaction list ID does not exist"]
        response_object = {
            'status': 'FAILED',
            'message': 'Can not get transaction list data',
            'errors': errors
        }
        return response_object, 200

    transaction_list_items = TransactionListItem.query.filter_by(
        transaction_list_id=id)
    items = {}

    for item in transaction_list_items:
        # Query Product
        product = Product.query.filter_by(
            id=item.product_id).first()

        transaction_list_item_key = str(item.id)
        items[transaction_list_item_key] = {}
        items[transaction_list_item_key]['product'] = {}
        items[transaction_list_item_key]['product']['value'] = str(
            product.id)
        items[transaction_list_item_key]['product']['label'] = product.name
        items[transaction_list_item_key]['product_price'] = str(
            item.product_price)
        items[transaction_list_item_key]['quantity'] = str(item.quantity)
        items[transaction_list_item_key]['total_amount'] = str(item.amount)

    transaction_list_data = {}
    transaction_list_data['id'] = str(transaction_list.id)
    transaction_list_data['customer_id'] = str(transaction_list.customer_id)
    transaction_list_data['notes'] = str(transaction_list.notes)
    transaction_list_data['total_amount'] = str(transaction_list.total_amount)
    transaction_list_data['transaction_list_date'] = str(
        transaction_list.transaction_list_date).split(' ')[0]
    transaction_list_data['created_on'] = str(transaction_list.created_on)
    transaction_list_data['updated_on'] = str(transaction_list.updated_on)
    transaction_list_data['transaction_list_items'] = items

    response_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully getting transaction list data',
        'data': transaction_list_data
    }
    return response_object, 200


def get_all_transaction_lists_with_pagination(args):
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
        transaction_lists = TransactionList.query.order_by(
            TransactionList.created_on.desc())
    else:
        if sort_order == -1:
            transaction_lists = TransactionList.query.order_by(
                desc(sort_field))
        else:
            transaction_lists = TransactionList.query.order_by(asc(sort_field))

    transaction_lists_on_page = transaction_lists.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(transaction_lists.count() / page_size)

    if math.ceil(transaction_lists.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for transaction_list in transaction_lists_on_page:
        # Sort by keyword
        if (key_word is not None):
            if (key_word in str(transaction_list.customer_id)) or (
                    key_word in str(transaction_list.transaction_list_date)):
                transaction_list_data = {}
                transaction_list_data['id'] = str(transaction_list.id)
                transaction_list_data['customer_id'] = str(
                    transaction_list.customer_id)
                transaction_list_data['notes'] = str(transaction_list.notes)
                transaction_list_data['total_amount'] = str(
                    transaction_list.total_amount)
                transaction_list_data['transaction_list_date'] = str(
                    transaction_list.transaction_list_date).split(' ')[0]

                output.append(transaction_list_data)
        else:
            transaction_list_data = {}
            transaction_list_data['id'] = str(transaction_list.id)
            transaction_list_data['customer_id'] = str(
                transaction_list.customer_id)
            transaction_list_data['notes'] = str(transaction_list.notes)
            transaction_list_data['total_amount'] = str(
                transaction_list.total_amount)
            transaction_list_data['transaction_list_date'] = str(
                transaction_list.transaction_list_date).split(' ')[0]

            output.append(transaction_list_data)

    data = {}
    data['transaction_lists'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all transaction_lists',
        'data': data
    }
    return response_object, 200


def get_all_transaction_list_data():
    all_transaction_list_data = TransactionList.query.all()
    output = []

    for trsc_list in all_transaction_list_data:
        trsc_list_data = {}
        trsc_list_data['id'] = str(trsc_list.id)
        trsc_list_data['customer_id'] = str(trsc_list.customer_id)
        trsc_list_data['total_amount'] = str(trsc_list.total_amount)
        trsc_list_data['transaction_list_date'] = str(
            trsc_list.transaction_list_date).split(' ')[0]
        trsc_list_data['created_on'] = str(trsc_list.created_on)
        trsc_list_data['updated_on'] = str(trsc_list.updated_on)

        output.append(trsc_list_data)

    data = {}
    data['transaction_lists'] = output

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all transaction lists',
        'data': data
    }
    return response_object, 200


def update_transaction_list_data(id, data):
    transaction = TransactionList.query.filter_by(id=id).first()
    transaction_items = TransactionListItem.query.filter_by(
        transaction_list_id=id)
    is_updated = False
    errors = {}

    if not transaction:
        errors['id'] = ["Transaction list ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': 'Cannot update transaction list data!',
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['customer_id'] == "":
            errors['customer_id'] = ["Customer id must not be null"]

        if data['transaction_list_date'] == "":
            errors['transaction_list_date'] = [
                "Transaction date must not be null"]

        for item in data['transaction_list_items']:
            # Check if foregin key "product_id" is valid or not
            product_id = item['product']['value']
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                errors['product_id'] = [
                    "Product id " + product_id + " is not valid"]

            if item['quantity'] == "":
                errors['price'] = ["Transaction item price can not be null"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update transaction list data!",
                'errors': errors
            }
            return response_object, 200
        else:
            # Update inware list
            if data['customer_id'] != transaction.customer_id:
                is_updated = True
                transaction.customer_id = data['customer_id']

            dt_trs_date = datetime.datetime.strptime(
                data['transaction_list_date'], '%Y-%m-%d')
            if dt_trs_date != transaction.transaction_list_date:
                is_updated = True
                transaction.transaction_list_date = dt_trs_date

            # For loop to update inware list items
            db_items = []
            request_items = []
            i_total_amount = transaction.total_amount
            for db_item in transaction_items:
                db_items.append(db_item.product_id)

            for item in data['transaction_list_items']:
                # Compare product_id in request with others in db
                # If has, compare quantiy
                p_id = item['product']['value']
                i_quantity = int(item["quantity"])

                request_items.append(p_id)

                if p_id in str(db_items):
                    transaction_list_item = TransactionListItem.query.filter_by(
                        transaction_list_id=id, product_id=p_id).first()

                    if i_quantity != transaction_list_item.quantity:
                        i_total_amount -= transaction_list_item.amount
                        transaction_list_item.quantity = i_quantity
                        transaction_list_item.amount = i_quantity*transaction_list_item.product_price
                        i_total_amount += transaction_list_item.amount
                        is_updated = True
                else:
                    is_updated = True
                    # If does not aldready exist, add new
                    product_sale_price = calc_the_nearest_sale_price(
                        item['product']['value'], id)
                    new_transaction_list_item = TransactionListItem(
                        transaction_list_id=id,
                        product_id=item['product']['value'],
                        product_price=product_sale_price,
                        quantity=i_quantity,
                        amount=product_sale_price*i_quantity,
                        created_on=datetime.datetime.utcnow(),
                        updated_on=datetime.datetime.utcnow()
                    )
                    db.session.add(new_transaction_list_item)
                    i_total_amount += new_transaction_list_item.amount

            for db_item in transaction_items:
                # Check if product_id is not exist in request, then delete
                if not (str(db_item.product_id) in request_items):
                    i_total_amount -= db_item.amount
                    db.session.delete(db_item)
                    is_updated = True

            if is_updated is True:
                transaction.total_amount = i_total_amount
                transaction.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated transaction list data",
            }
            return response_object, 200


def delete_transaction_list_data(id):
    errors = {}
    # Delete transaction items
    transaction_list_items = TransactionListItem.query.filter_by(
        transaction_list_id=id)
    transaction_list = TransactionList.query.filter_by(
        id=id).first()

    if ((not transaction_list) or (not transaction_list_items)):
        errors = ['Transaction list ID is not valid']
        respone_object = {
            'status': 'ERROR',
            'message': 'Can not delete transaction list data!',
            'error:': errors
        }
        return respone_object, 200
    else:
        for item in transaction_list_items:
            db.session.delete(item)

        db.session.delete(transaction_list)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted transaction list data!'
        }
        return response_object, 200


def get_all_products_lastest_price():
    all_products = Product.query.all()

    output = {}

    for product in all_products:
        output[str(product.id)] = int(calc_latest_sale_price(product.id))

    response_object = {
        'status': 'SUCCESS',
        'message': 'Sucessfully getting product latest price!',
        'data': output
    }
    return response_object, 200


def calc_latest_sale_price(product_id):
    product_price_history = ProductPriceHistory.query.filter_by(
        product_id=product_id)

    backward_time = []
    for product_price in product_price_history:
        backward_time.append(product_price.effective_date)

    if not backward_time:
        return 0
    else:
        nearest_date = max(backward_time)

        product_nearest_price = ProductPriceHistory.query.filter_by(
            product_id=product_id, effective_date=nearest_date).first()

        return product_nearest_price.sale_price

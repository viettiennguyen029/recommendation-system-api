import datetime
import math

from app.main import db
from sqlalchemy import desc, asc

from app.main.model.product import Product
from app.main.model.recommended_list import RecommendedList
from app.main.model.recommended_list_item import RecommendedListItem


def save_recommended_list_data(data):
    errors = {}
    # Check null
    if data['title'] == "":
        errors['title'] = ['Title must not be null!']

    if data['total_products'] == "":
        errors['total_products'] = ['Total product must not be null!']

    if data['time_span'] == "":
        errors['time_span'] = ['Time span must not be null!']

    # for rcm_list_item in data['recommended_list_items']:
    #     # Check foregin key - product
    #     product = Product.query.filter_by(
    #         id=rcm_list_item['product']['value']).first()
    #     if not product:
    #         errors['product'] = ["Product ID does not exist!"]

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new recommended list',
            'errors': errors
        }
        return response_object, 200
    else:
        new_recommended_list = RecommendedList(
            title=data['title'],
            description=data['description'],
            total_products=data['total_products'],
            time_span_month=data['time_span']['month'],
            time_span_year=data['time_span']['year'],
            created_on=datetime.datetime.utcnow(),
            updated_on=datetime.datetime.utcnow()
        )
        db.session.add(new_recommended_list)
        db.session.commit()

        for item in data['recommended_list_items']:
            new_recommended_list_item = RecommendedListItem(
                recommended_list_id=str(new_recommended_list.id),
                product_id=item['product']['value'],
                quantity=item['quantity'],
                min_quantity=item['min_quantity'],
                max_quantity=item['max_quantity'],
                revenue=item['revenue'],
                min_revenue=item['min_revenue'],
                max_revenue=item['max_revenue'],
                accuracy=item['accuracy'],
                priority=item['priority'],
                original_price=item['original_price'],
                sale_price=item['sale_price'],
                profit_rate=item['profit_rate'],
                inware_amount=item['inware_amount'],
                min_inware_amount=item['min_inware_amount'],
                max_inware_amount=item['max_inware_amount'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            db.session.add(new_recommended_list_item)
            db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'A new new recommended list is created successfully!'
        }
        return response_object, 201


def get_all_recommended_list_data():
    all_recommended_list = RecommendedList.query.all()
    output = []

    for rcm_list in all_recommended_list:
        recommended_list_data = {}
        recommended_list_data['id'] = str(rcm_list.id)
        recommended_list_data['title'] = rcm_list.title
        recommended_list_data['description'] = rcm_list.description
        recommended_list_data['time_span'] = {}
        recommended_list_data['time_span']['year'] = str(
            rcm_list.time_span_year)
        recommended_list_data['time_span']['month'] = str(
            rcm_list.time_span_month)
        recommended_list_data['created_on'] = str(rcm_list.created_on)
        recommended_list_data['updated_on'] = str(rcm_list.updated_on)

        output.append(recommended_list_data)

    data = {}
    data['recommended_list'] = output

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all recommended lists',
        'data': data
    }
    return response_object, 200

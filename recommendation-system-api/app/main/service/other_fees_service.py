import datetime
import math

from sqlalchemy import desc, asc
from app.main import db
from app.main.model.other_fees import OtherFees


def save_other_fees(data):
    errors = {}

    # Check null
    if data['started_on'] == "":
        errors['started_on'] = 'Other fee start day must not be null!'

    if data['ended_on'] == "":
        errors['ended_on'] = 'Other fee end day must not be null!'

    if data['amount'].isnumeric() is False:
        errors['amount'] = 'Other fee amount is not valid!'

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new other fees!',
            'errors': errors
        }
        return response_object, 200
    else:
        started_day = datetime.datetime.strptime(
            data['started_on'], '%Y-%m-%d')

        ended_day = datetime.datetime.strptime(
            data['ended_on'], '%Y-%m-%d')

        other_fees = OtherFees.query.filter_by(
            started_on=started_day, ended_on=ended_day).first()

        if other_fees:
            errors['name'] = 'Other fees is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a other fees!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_other_fees = OtherFees(
                amount=data['amount'],
                started_on=started_day,
                ended_on=ended_day,
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            db.session.add(new_other_fees)
            db.session.commit()

            output = {}
            output['started_on'] = str(new_other_fees.started_on)
            output['ended_on'] = str(new_other_fees.ended_on)
            output['amount'] = str(new_other_fees.amount)
            output['created_on'] = str(new_other_fees.created_on)
            output['updated_on'] = str(new_other_fees.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new other fees is created successfully!',
                'data': output
            }
            return response_object, 201


def get_other_fees(id):
    errors = {}
    other_fees = OtherFees.query.filter_by(id=id).first()

    if other_fees:
        other_fees_data = {}
        other_fees_data['id'] = str(other_fees.id)
        other_fees_data['started_on'] = str(other_fees.started_on)
        other_fees_data['ended_on'] = str(other_fees.ended_on)
        other_fees_data['amount'] = str(other_fees.amount)
        other_fees_data['created_on'] = str(other_fees.created_on)
        other_fees_data['updated_on'] = str(other_fees.updated_on)

        response_object = {
            'status': 'SUCCESS',
            'message':  'Sucessfully getting other fees data',
            'data': other_fees_data
        }
        return response_object, 200
    else:
        errors['id'] = ["Other fees ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not get other fees data",
            'errors': errors
        }
        return response_object, 200


def delete_other_fees(id):
    errors = {}
    other_fees = OtherFees.query.filter_by(id=id).first()

    if other_fees:
        db.session.delete(other_fees)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted the other fees!'
        }
        return response_object, 200
    else:
        errors['id'] = ["Other fees ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not delete other fees",
            'errors': errors
        }
        return response_object, 200


def update_other_fees(id, data):
    other_fees_id = OtherFees.query.filter_by(id=id).first()
    is_updated = False
    errors = {}

    # Check if ID is valid or not
    if not other_fees_id:
        errors['id'] = ["Other fee's ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not update other fees data!",
            'errors': errors
        }
        return response_object, 200
    else:
        # Check type
        if data['amount'].isnumeric() is False:
            errors['amount'] = ["Amount is not valid!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update other fees data!",
                'errors': errors
            }
            return response_object, 200
        else:
            # Check if start day and end day is existed or not
            started_day = datetime.datetime.strptime(
                data['started_on'], '%Y-%m-%d')

            ended_day = datetime.datetime.strptime(
                data['ended_on'], '%Y-%m-%d')

            if (started_day != other_fees_id.started_on or
                    ended_day != other_fees_id.ended_on):

                other_fees = OtherFees.query.filter_by(
                    started_on=started_day, ended_on=ended_day).first()

                if other_fees:
                    errors['started_on'] = ["Other fees is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update other fees data!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    other_fees_id.started_on = started_day
                    other_fees_id.ended_on = ended_day

            if data['amount'] != str(other_fees_id.amount):
                is_updated = True
                other_fees_id.amount = data['amount']

            if is_updated is True:
                other_fees_id.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            other_fees_data = {}
            other_fees_data['id'] = str(other_fees_id.id)
            other_fees_data['started_on'] = str(other_fees_id.started_on)
            other_fees_data['ended_on'] = str(other_fees_id.ended_on)
            other_fees_data['amount'] = str(other_fees_id.amount)
            other_fees_data['created_on'] = str(other_fees_id.created_on)
            other_fees_data['updated_on'] = str(other_fees_id.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated other_fees data!",
                'data': other_fees_data
            }
            return response_object, 200


def get_all_other_fees_with_pagination(args):
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
        others_fees = OtherFees.query.order_by(
            OtherFees.created_on.desc())
    else:
        if sort_order == -1:
            others_fees = OtherFees.query.order_by(
                desc(sort_field))
        else:
            others_fees = OtherFees.query.order_by(
                asc(sort_field))

    other_fees_on_page = others_fees.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(others_fees.count() / page_size)

    if math.ceil(others_fees.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for other_fee in other_fees_on_page:
        # Sort by keyword
        if (key_word is not None):
            if (key_word in str(other_fee.started_on) or (
                    key_word in str(other_fee.ended_on))):
                other_fees_data = {}
                other_fees_data['id'] = str(other_fee.id)
                other_fees_data['started_on'] = str(other_fee.started_on)
                other_fees_data['ended_on'] = str(other_fee.ended_on)
                other_fees_data['amount'] = str(other_fee.amount)
                other_fees_data['created_on'] = str(other_fee.created_on)
                other_fees_data['updated_on'] = str(other_fee.updated_on)

                output.append(other_fees_data)
        else:
            other_fees_data = {}
            other_fees_data['id'] = str(other_fee.id)
            other_fees_data['started_on'] = str(other_fee.started_on)
            other_fees_data['ended_on'] = str(other_fee.ended_on)
            other_fees_data['amount'] = str(other_fee.amount)
            other_fees_data['created_on'] = str(other_fee.created_on)
            other_fees_data['updated_on'] = str(other_fee.updated_on)

            output.append(other_fees_data)

    data = {}
    data['others_fees'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all others fees',
        'data': data
    }
    return response_object, 200

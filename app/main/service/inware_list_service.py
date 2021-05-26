import datetime
import math

from sqlalchemy import desc, asc
from app.main import db
from app.main.model.inware_list import InwareList


def save_inware_list(data):
    errors = {}

    # Check null
    if data['name'] == "":
        errors['name'] = "Inware list name must not be null!"

    if data['record_date'] == "":
        errors['record_date'] = 'Inware list record date must not be null!'

    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new inware list!',
            'errors': errors
        }
        return response_object, 200
    else:
        inware_list = InwareList.query.filter_by(
            name=data['name']).first()

        if inware_list:
            errors['name'] = 'Inware list name is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a new inware list!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_inware_list = InwareList(
                name=data['name'],
                description=data['description'],
                record_date=datetime.datetime.strptime(
                    data['record_date'], '%Y-%m-%d'),
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            db.session.add(new_inware_list)
            db.session.commit()

            output = {}
            output['name'] = new_inware_list.name
            output['description'] = new_inware_list.description
            output['record_date'] = str(new_inware_list.record_date)
            output['created_on'] = str(new_inware_list.created_on)
            output['updated_on'] = str(new_inware_list.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new inware list is created successfully!',
                'data': output
            }
            return response_object, 201


def get_inware_list(id):
    errors = {}
    inware_list = InwareList.query.filter_by(id=id).first()

    if inware_list:
        inware_list_data = {}
        inware_list_data['id'] = str(inware_list.id)
        inware_list_data['name'] = inware_list.name
        inware_list_data['description'] = inware_list.description
        inware_list_data['created_on'] = str(inware_list.created_on)
        inware_list_data['updated_on'] = str(inware_list.updated_on)

        response_object = {
            'status': 'SUCCESS',
            'message':  'Successfully getting inware list data',
            'data': inware_list_data
        }
        return response_object, 200

    else:
        errors['id'] = ["inware list ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not get inware list data",
            'errors': errors
        }
        return response_object, 200


def delete_inware_list(id):
    errors = {}
    inware_list = InwareList.query.filter_by(id=id).first()

    if not inware_list:
        errors['id'] = ["inware list ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not delete inware list",
            'errors': errors
        }
        return response_object, 200
    else:
        db.session.delete(inware_list)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted inware list data!'
        }
        return response_object, 200


def get_all_inware_lists_with_pagination(args):
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
                inware_list_data['description'] = inware_list.description
                inware_list_data['record_date'] = str(inware_list.record_date)
                inware_list_data['created_on'] = str(inware_list.created_on)
                inware_list_data['updated_on'] = str(inware_list.updated_on)

                output.append(inware_list_data)
        else:
            inware_list_data = {}
            inware_list_data['id'] = str(inware_list.id)
            inware_list_data['name'] = inware_list.name
            inware_list_data['description'] = inware_list.description
            inware_list_data['record_date'] = str(inware_list.record_date)
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


def update_inware_list(id, data):
    inware_list_id = InwareList.query.filter_by(id=id).first()
    is_updated = False
    errors = {}

    # Check if ID is valid or not
    if not inware_list_id:
        errors['id'] = ["inware list ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not update inware list data!",
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == '':
            errors['name'] = ["Inware list name must not be null!"]

        if data['record_date'] == '':
            errors['record_date'] = ["Inware list record date must not be null!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update inware list data!",
                'errors': errors
            }
            return response_object, 200
        else:
            if data['name'] != inware_list_id.name:
                # Check if inware_list name is existed or not
                inware_list = InwareList.query.filter_by(
                    name=data['name']).first()
                if inware_list:
                    errors['name'] = ["Inware list name is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update inware_list's information!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    inware_list_id.name = data['name']

            if data['description'] != inware_list_id.description:
                is_updated = True
                inware_list_id.description = data['description']

            record_date_value = datetime.datetime.strptime(
                    data['record_date'], '%Y-%m-%d')
            if record_date_value != inware_list_id.record_date:
                is_updated = True
                inware_list_id.record_date = record_date_value

            if is_updated is True:
                inware_list_id.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            inware_list_data = {}
            inware_list_data['id'] = str(inware_list_id.id)
            inware_list_data['name'] = inware_list_id.name
            inware_list_data['description'] = inware_list_id.description
            inware_list_data['record_date'] = str(inware_list_id.record_date)
            inware_list_data['created_on'] = str(inware_list_id.created_on)
            inware_list_data['updated_on'] = str(inware_list_id.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated inware list data!",
                'data': inware_list_data
            }
            return response_object, 200

import datetime
import math

from sqlalchemy import desc, asc

from app.main import db
from app.main.model.unit import Unit
from app.main.service.language_helper import LanguageHelper


def save_unit(data, args):
    errors = {}
    language_data = LanguageHelper(args)

    # Check unique field is null or not
    if data['name'] == "":
        errors['name'] = [language_data.get_message(
            'unit.save.no_unit_name_message')]
    if len(errors) > 0:
        response_object = {
            'status': 'FAILED',
            'message': language_data.get_message('unit.save.failed_message'),
            'errors': errors
        }
        return response_object, 200
    else:
        unit = Unit.query.filter_by(
            name=data['name']).first()

        if unit:
            errors['name'] = [language_data.get_message(
                'unit.save.existed_unit_name_message')]
            response_object = {
                'status': 'FAILED',
                'message': language_data.get_message('unit.save.failed_message'),
                'errors': errors
            }
            return response_object, 200
        else:
            new_unit = Unit(
                name=data['name'],
                description=data['description'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            save_changes(new_unit)

            output = {}
            output['name'] = new_unit.name
            output['description'] = new_unit.description
            output['created_on'] = str(new_unit.created_on)
            output['updated_on'] = str(new_unit.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': language_data.get_message('unit.save.success_message'),
                'data': output
            }
            return response_object, 201


def update_unit(id, data, args):
    unit = Unit.query.filter_by(id=id).first()
    is_updated = False
    errors = {}
    language_data = LanguageHelper(args)

    # Check if ID is valid or not
    if not unit:
        errors['id'] = ["Unit ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': language_data.get_message('unit.update.failed_message'),
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == "":
            errors['name'] = [language_data.get_message(
                'unit.update.no_unit_message')]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': language_data.get_message('unit.update.failed_message'),
                'errors': errors
            }
            return response_object, 200
        else:
            if data['name'] != unit.name:
                # Check if unit name is existed or not
                updated_unit = Unit.query.filter_by(name=data['name']).first()
                if updated_unit:
                    errors['name'] = [language_data.get_message(
                        'unit.update.existed_unit_name_message')]
                    response_object = {
                        'status': 'FAILED',
                        'message': language_data.get_message('unit.update.failed_message'),
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    unit.name = data['name']

            if data['description'] != unit.description:
                is_updated = True
                unit.description = data['description']

            if is_updated is True:
                unit.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            unit_data = {}
            unit_data['id'] = str(unit.id)
            unit_data['name'] = unit.name
            unit_data['description'] = unit.description
            unit_data['created_on'] = str(unit.created_on)
            unit_data['updated_on'] = str(unit.updated_on)

            respone_object = {
                'status': 'SUCCESS',
                'message': language_data.get_message('unit.update.success_message'),
                'data': unit_data
            }
            return respone_object, 200


def get_all_units(args):
    all_unit = Unit.query.all()
    output = []
    languages_data = LanguageHelper(args)

    for unit in all_unit:
        unit_data = {}
        unit_data['id'] = unit.id
        unit_data['name'] = unit.name
        unit_data['description'] = unit.description
        unit_data['created_on'] = str(unit.created_on)
        unit_data['updated_on'] = str(unit.updated_on)

        output.append(unit_data)

    data = {}
    data['units'] = output

    respone_object = {
        'status': 'SUCCESS',
        'message':  languages_data.get_message('unit.get_all.success_message'),
        'data': data
    }
    return respone_object, 200


def get_unit(id, args):
    unit = Unit.query.filter_by(id=id).first()
    languages_data = LanguageHelper(args)

    if not unit:
        respone_object = {
            'status': 'ERROR',
            'message': languages_data.get_message('unit.get.no_unit_message')
        }
        return respone_object, 200

    unit_data = {}
    unit_data['id'] = unit.id
    unit_data['name'] = unit.name
    unit_data['description'] = unit.description
    unit_data['created_on'] = str(unit.created_on)
    unit_data['updated_on'] = str(unit.updated_on)

    respone_object = {
        'status': 'SUCCESS',
        'message':  languages_data.get_message('unit.delete.success_message'),
        'data': unit_data
    }
    return respone_object, 200


def delete_unit(id, args):
    errors = {}
    unit = Unit.query.filter_by(id=id).first()
    languages_data = LanguageHelper(args)

    if not unit:
        respone_object = {
            'status': 'FAILED',
            'message': languages_data.get_message('unit.delete.no_unit_message'),
            'errors': errors
        }
        return respone_object, 200
    else:
        db.session.delete(unit)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': languages_data.get_message('unit.delete.success_message')
        }
        return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def get_all_units_with_pagination(args):
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

    # Get language data
    languages_data = LanguageHelper(args)

    # Sort by order value
    if sort_field is None or sort_order is None:
        '''Default order by the lasted created_on value'''
        units = Unit.query.order_by(Unit.created_on.desc())
    else:
        if sort_order == -1:
            units = Unit.query.order_by(desc(sort_field))
        else:
            units = Unit.query.order_by(asc(sort_field))

    units_on_page = units.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(units.count() / page_size)

    if math.ceil(units.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for unit in units_on_page:
        # Sort by keyword
        if (key_word is not None):
            if (key_word in unit.name.lower()) or (
                    key_word in unit.description.lower()):
                unit_data = {}
                unit_data['id'] = unit.id
                unit_data['name'] = unit.name
                unit_data['description'] = unit.description
                unit_data['created_on'] = str(unit.created_on)
                unit_data['updated_on'] = str(unit.updated_on)

                output.append(unit_data)
        else:
            unit_data = {}
            unit_data['id'] = unit.id
            unit_data['name'] = unit.name
            unit_data['description'] = unit.description
            unit_data['created_on'] = str(unit.created_on)
            unit_data['updated_on'] = str(unit.updated_on)

            output.append(unit_data)

    data = {}
    data['units'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  languages_data.get_message('unit.get_all_with_pagination.success_message'),
        'data': data
    }
    return response_object, 200

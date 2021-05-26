import datetime
import math

from sqlalchemy import desc, asc
from app.main import db
from app.main.model.manufacturer import Manufacturer


def save_manufacturer(data):
    errors = {}

    # Check null
    if data['name'] == "":
        errors['name'] = 'Manufacturer name must not be null!'

    if data['email'] == "":
        errors['email'] = 'Manufacturer email must not be null!'

    if data['address'] == "":
        errors['address'] = 'Manufacturer address must not be null!'

    if data['phone_number'] == "":
        errors['phone_number'] = 'Manufacturer phone number must not be null!'

    if data['fax_number'] == "":
        errors['fax_number'] = 'Manufacturer fax number must not be null!'

    if len(errors) > 0:
        respone_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new manufacturer!',
            'errors': errors
        }
        return respone_object, 200
    else:
        manufacturer = Manufacturer.query.filter_by(
            name=data['name']).first()

        if manufacturer:
            errors['name'] = 'Manufacturer name is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a new manufacturer!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_manufacturer = Manufacturer(
                name=data['name'],
                description=data['description'],
                address=data['address'],
                email=data['email'],
                phone_number=data['phone_number'],
                fax_number=data['fax_number'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            save_changes(new_manufacturer)

            output = {}
            output['name'] = new_manufacturer.name
            output['description'] = new_manufacturer.description
            output['email'] = new_manufacturer.email
            output['address'] = new_manufacturer.address
            output['phone_number'] = new_manufacturer.phone_number
            output['fax_number'] = new_manufacturer.fax_number
            output['created_on'] = str(new_manufacturer.created_on)
            output['updated_on'] = str(new_manufacturer.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new Manufacturer is created successfully!',
                'data': output
            }
            return response_object, 201


def update_manufacturer(id, data):
    manufacturer = Manufacturer.query.filter_by(id=id).first()
    is_updated = False
    errors = {}

    # Check if ID is valid or not
    if not manufacturer:
        errors['id'] = ["Manufacturer ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not update manufacturer's information!",
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == '':
            errors['name'] = ["Manufacturer name must not be null!"]

        if data['email'] == "":
            errors['email'] = 'Manufacturer email must not be null!'

        if data['phone_number'] == "":
            errors['phone_number'] = 'Manufacturer phone number must not be null!'

        if data['fax_number'] == "":
            errors['fax_number'] = 'Manufacturer fax number must not be null!'

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update manufacturer's information!",
                'errors': errors
            }
            return response_object, 200
        else:
            if data['name'] != manufacturer.name:
                # Check if manufacturer name is existed or not
                updated_manufacturer = Manufacturer.query.filter_by(
                    name=data['name']).first()
                if updated_manufacturer:
                    errors['name'] = ["Manufacturer name is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update manufacturer's information!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    manufacturer.name = data['name']

            if data['description'] != manufacturer.description:
                is_updated = True
                manufacturer.description = data['description']

            if data['email'] != manufacturer.email:
                is_updated = True
                manufacturer.email = data['email']

            if data['address'] != manufacturer.address:
                is_updated = True
                manufacturer.address = data['address']

            if data['phone_number'] != manufacturer.phone_number:
                is_updated = True
                manufacturer.phone_number = data['phone_number']

            if data['fax_number'] != manufacturer.fax_number:
                is_updated = True
                manufacturer.fax_number = data['fax_number']

            if is_updated is True:
                manufacturer.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            manufacturer_data = {}
            manufacturer_data['id'] = str(manufacturer.id)
            manufacturer_data['name'] = manufacturer.name
            manufacturer_data['description'] = manufacturer.description
            manufacturer_data['email'] = manufacturer.email
            manufacturer_data['address'] = manufacturer.address
            manufacturer_data['phone_number'] = manufacturer.phone_number
            manufacturer_data['fax_number'] = manufacturer.fax_number
            manufacturer_data['created_on'] = str(manufacturer.created_on)
            manufacturer_data['updated_on'] = str(manufacturer.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated manufacturer information!",
                'data': manufacturer_data
            }
            return response_object, 200


def get_all_manufacturers():
    all_manufacturer = Manufacturer.query.all()
    output = []

    for manufacture in all_manufacturer:
        manufacture_data = {}
        manufacture_data['id'] = manufacture.id
        manufacture_data['name'] = manufacture.name
        manufacture_data['description'] = manufacture.description
        manufacture_data['email'] = manufacture.email
        manufacture_data['address'] = manufacture.address
        manufacture_data['phone_number'] = manufacture.phone_number
        manufacture_data['fax_number'] = manufacture.fax_number
        manufacture_data['created_on'] = str(manufacture.created_on)
        manufacture_data['updated_on'] = str(manufacture.updated_on)

        output.append(manufacture_data)

    data = {}
    data['manufacturer'] = output

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all manufactures',
        'data': data
    }
    return respone_object, 200


def get_manufacturer(id):
    errors = {}
    manufacturer = Manufacturer.query.filter_by(id=id).first()

    if not manufacturer:
        errors['id'] = ["Manufacturer ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not get manufacturer's information",
            'errors': errors
        }
        return response_object, 200

    manufacturer_data = {}
    manufacturer_data['id'] = str(manufacturer.id)
    manufacturer_data['name'] = manufacturer.name
    manufacturer_data['description'] = manufacturer.description
    manufacturer_data['email'] = manufacturer.email
    manufacturer_data['address'] = manufacturer.address
    manufacturer_data['phone_number'] = manufacturer.phone_number
    manufacturer_data['fax_number'] = manufacturer.fax_number
    manufacturer_data['created_on'] = str(manufacturer.created_on)
    manufacturer_data['updated_on'] = str(manufacturer.updated_on)

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of manufacturer',
        'data': manufacturer_data
    }
    return response_object, 200


def delete_manufacturer(id):
    errors = {}
    manufacturer = Manufacturer.query.filter_by(id=id).first()

    if not manufacturer:
        errors['id'] = ["Manufacturer ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not delete manufacturer",
            'errors': errors
        }
        return response_object, 200
    else:
        db.session.delete(manufacturer)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted the manufacturer!'
        }
        return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def get_all_manufacturers_with_pagination(args):
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
        manufacturers = Manufacturer.query.order_by(
            Manufacturer.created_on.desc())
    else:
        if sort_order == -1:
            manufacturers = Manufacturer.query.order_by(
                desc(sort_field))
        else:
            manufacturers = Manufacturer.query.order_by(
                asc(sort_field))

    manufacturers_on_page = manufacturers.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(manufacturers.count() / page_size)

    if math.ceil(manufacturers.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for manufacturer in manufacturers_on_page:
        # Sort by keyword
        if (key_word is not None):
            if (key_word in manufacturer.name.lower()) or (
                    key_word in manufacturer.description.lower()) or (
                        key_word in manufacturer.email.lower()) or (
                            key_word in manufacturer.phone_number):
                manufacturer_data = {}
                manufacturer_data['id'] = str(manufacturer.id)
                manufacturer_data['name'] = manufacturer.name
                manufacturer_data['description'] = manufacturer.description
                manufacturer_data['email'] = manufacturer.email
                manufacturer_data['address'] = manufacturer.address
                manufacturer_data['phone_number'] = manufacturer.phone_number
                manufacturer_data['fax_number'] = manufacturer.fax_number
                manufacturer_data['created_on'] = str(manufacturer.created_on)
                manufacturer_data['updated_on'] = str(manufacturer.updated_on)

                output.append(manufacturer_data)
        else:
            manufacturer_data = {}
            manufacturer_data['id'] = str(manufacturer.id)
            manufacturer_data['name'] = manufacturer.name
            manufacturer_data['description'] = manufacturer.description
            manufacturer_data['email'] = manufacturer.email
            manufacturer_data['address'] = manufacturer.address
            manufacturer_data['phone_number'] = manufacturer.phone_number
            manufacturer_data['fax_number'] = manufacturer.fax_number
            manufacturer_data['created_on'] = str(manufacturer.created_on)
            manufacturer_data['updated_on'] = str(manufacturer.updated_on)

            output.append(manufacturer_data)

    data = {}
    data['manufacturers'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all manufacturers',
        'data': data
    }
    return response_object, 200

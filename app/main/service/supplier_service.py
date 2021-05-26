import datetime
import math

from sqlalchemy import desc, asc
from app.main import db
from app.main.model.supplier import Supplier


def save_supplier(data):
    errors = {}

    # Check null
    if data['name'] == "":
        errors['name'] = ['Supplier name must not be null!']

    if data['address'] == "":
        errors['address'] = ['Supplier address must not be null!']

    if data['email'] == "":
        errors['email'] = ['Supplier email must not be null!']

    if data['phone_number'] == "":
        errors['phone_number'] = ['Supplier phone number must not be null!']

    if data['fax_number'] == "":
        errors['fax_number'] = ['Supplier fax number must not be null!']

    if len(errors) > 0:
        respone_object = {
            'status': 'FAILED',
            'message': 'Failed to create a new supplier!',
            'errors': errors
        }
        return respone_object, 200
    else:
        supplier = Supplier.query.filter_by(
            name=data['name']).first()

        if supplier:
            errors['name'] = 'Supplier name is already existed!'
            response_object = {
                'status': 'FAILED ',
                'message': 'Failed to create a new supplier!',
                'errors': errors
            }
            return response_object, 200
        else:
            new_supplier = Supplier(
                name=data['name'],
                description=data['description'],
                address=data['address'],
                email=data['email'],
                phone_number=data['phone_number'],
                fax_number=data['fax_number'],
                created_on=datetime.datetime.utcnow(),
                updated_on=datetime.datetime.utcnow()
            )
            save_changes(new_supplier)

            output = {}
            output['name'] = new_supplier.name
            output['description'] = new_supplier.description
            output['address'] = new_supplier.address
            output['email'] = new_supplier.email
            output['phone_number'] = new_supplier.phone_number
            output['fax_number'] = new_supplier.fax_number
            output['created_on'] = str(new_supplier.created_on)
            output['updated_on'] = str(new_supplier.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': 'A new supplier is created successfully!',
                'data': output
            }
            return response_object, 201


def update_supplier(id, data):
    supplier = Supplier.query.filter_by(id=id).first()
    is_updated = False
    errors = {}

    # Check if ID is valid or not
    if not supplier:
        errors['id'] = ["Supplier ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not update supplier data!",
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['name'] == '':
            errors['name'] = ["Supplier name must not be null!"]

        if data['address'] == '':
            errors['address'] = ["Supplier address must not be null!"]

        if data['email'] == '':
            errors['email'] = ["Supplier email must not be null!"]

        if data['phone_number'] == '':
            errors['phone_number'] = [
                "Supplier phone number must not be null!"]

        if data['fax_number'] == '':
            errors['fax_number'] = ["Supplier fax number must not be null!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update supplier's information!",
                'errors': errors
            }
            return response_object, 200
        else:
            if data['name'] != supplier.name:
                # Check if supplier name is existed or not
                updated_supplier = Supplier.query.filter_by(
                    name=data['name']).first()
                if updated_supplier:
                    errors['name'] = ["Supplier name is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update supplier's information!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    supplier.name = data['name']

            if data['description'] != supplier.description:
                is_updated = True
                supplier.description = data['description']

            if data['address'] != supplier.address:
                is_updated = True
                supplier.address = data['address']

            if data['email'] != supplier.email:
                is_updated = True
                supplier.email = data['email']

            if data['phone_number'] != supplier.phone_number:
                is_updated = True
                supplier.phone_number = data['phone_number']

            if data['fax_number'] != supplier.phone_number:
                is_updated = True
                supplier.phone_number = data['fax_number']

            if is_updated is True:
                supplier.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            supplier_data = {}
            supplier_data['name'] = supplier.name
            supplier_data['description'] = supplier.description
            supplier_data['address'] = supplier.address
            supplier_data['email'] = supplier.email
            supplier_data['phone_number'] = supplier.phone_number
            supplier_data['fax_number'] = supplier.phone_number
            supplier_data['created_on'] = str(supplier.created_on)
            supplier_data['updated_on'] = str(supplier.updated_on)

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully updated supplier information!",
                'data': supplier_data
            }
            return response_object, 200


def get_all_suppliers():
    all_supplier = Supplier.query.all()
    output = []

    for supplier in all_supplier:
        supplier_data = {}
        supplier_data['id'] = str(supplier.id)
        supplier_data['name'] = supplier.name
        supplier_data['description'] = supplier.description
        supplier_data['address'] = supplier.address
        supplier_data['email'] = supplier.email
        supplier_data['phone_number'] = supplier.phone_number
        supplier_data['fax_number'] = supplier.fax_number
        supplier_data['created_on'] = str(supplier.created_on)
        supplier_data['updated_on'] = str(supplier.updated_on)

        output.append(supplier_data)

    data = {}
    data['supplier'] = output

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all suppliers',
        'data': data
    }
    return respone_object, 200


def get_supplier(id):
    errors = {}
    supplier = Supplier.query.filter_by(id=id).first()

    if not supplier:
        errors['id'] = ["supplier ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not get supplier data",
            'errors': errors
        }
        return response_object, 200

    supplier_data = {}
    supplier_data['id'] = supplier.id
    supplier_data['name'] = supplier.name
    supplier_data['description'] = supplier.description
    supplier_data['address'] = supplier.address
    supplier_data['email'] = supplier.email
    supplier_data['phone_number'] = supplier.phone_number
    supplier_data['fax_number'] = supplier.fax_number
    supplier_data['created_on'] = str(supplier.created_on)
    supplier_data['updated_on'] = str(supplier.updated_on)

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of supplier',
        'data': supplier_data
    }
    return response_object, 200


def delete_supplier(id):
    errors = {}
    supplier = Supplier.query.filter_by(id=id).first()

    if not supplier:
        errors['id'] = ["Supplier ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not delete supplier",
            'errors': errors
        }
        return response_object, 200
    else:
        db.session.delete(supplier)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted the supplier!'
        }
        return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def get_all_suppliers_with_pagination(args):
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
        filtered_supplier = Supplier.query.order_by(
            Supplier.updated_on.desc())
    else:
        if sort_order == -1:
            filtered_supplier = Supplier.query.order_by(
                desc(sort_field))
        else:
            filtered_supplier = Supplier.query.order_by(
                asc(sort_field))

    suppliers_on_page = filtered_supplier.limit(page_size).offset(
        (current_page - 1) * page_size)
    total_pages = math.ceil(filtered_supplier.count() / page_size)

    if math.ceil(filtered_supplier.count() - page_size*current_page > 0):
        next_page = True
    else:
        next_page = False

    output = []

    for supplier in suppliers_on_page:
        # Sort by keyword
        if (key_word is not None):
            if (key_word.lower() in supplier.name.lower()) or (
                key_word.lower() in supplier.address.lower()) or (
                    key_word in supplier.phone_number) or (
                        key_word in supplier.description):
                supplier_data = {}
                supplier_data['id'] = supplier.id
                supplier_data['name'] = supplier.name
                supplier_data['description'] = supplier.description
                supplier_data['address'] = supplier.address
                supplier_data['email'] = supplier.email
                supplier_data['phone_number'] = supplier.phone_number
                supplier_data['fax_number'] = supplier.fax_number
                supplier_data['created_on'] = str(supplier.created_on)
                supplier_data['updated_on'] = str(supplier.updated_on)

                output.append(supplier_data)
        else:
            supplier_data = {}
            supplier_data['id'] = supplier.id
            supplier_data['name'] = supplier.name
            supplier_data['description'] = supplier.description
            supplier_data['address'] = supplier.address
            supplier_data['email'] = supplier.email
            supplier_data['phone_number'] = supplier.phone_number
            supplier_data['fax_number'] = supplier.fax_number
            supplier_data['created_on'] = str(supplier.created_on)
            supplier_data['updated_on'] = str(supplier.updated_on)

            output.append(supplier_data)

    data = {}
    data['suppliers'] = output
    data['total_pages'] = total_pages
    data['current_page'] = current_page
    data['has_next_page'] = next_page

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all suppliers',
        'data': data
    }
    return response_object, 200

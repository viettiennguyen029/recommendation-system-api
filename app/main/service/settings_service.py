import datetime

from app.main import db
from app.main.model.setting import Settings


def save_settings(data):
    errors = {}

    # Check unique field is null or not
    new_settings = Settings(
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        fax_number=data['phone_number'],
        address=data['address'],
        user_public_id=data['user_public_id'],
        billing_address=data['billing_address'],
        created_on=datetime.datetime.utcnow(),
        updated_on=datetime.datetime.utcnow()
    )
    db.session.add(new_settings)
    db.session.commit()

    response_object = {
        'status': 'SUCCESS',
        'message': "A new user's settings is created successfully!"
    }
    return response_object, 201


def get_settings(id):
    settings = Settings.query.filter_by(user_public_id=id).first()

    if not settings:
        response_object = {
            'status': 'ERROR',
            'message': 'Settings does not exist!'
        }
        return response_object, 200

    settings_data = {}
    settings_data['id'] = settings.id
    settings_data['full_name'] = settings.full_name
    settings_data['email'] = settings.email
    settings_data['phone_number'] = settings.phone_number
    settings_data['fax_number'] = settings.fax_number
    settings_data['address'] = settings.address
    settings_data['billing_address'] = settings.billing_address
    settings_data['created_on'] = str(settings.created_on)
    settings_data['updated_on'] = str(settings.updated_on)

    respone_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of settings',
        'data': settings_data
    }
    return respone_object, 200


def delete_settings(id):
    settings = Settings.query.filter_by(user_public_id=id).first()

    if not settings:
        respone_object = {
            'status': 'FAILED',
            'message': 'settings ID does not exist!'
        }
        return respone_object, 200
    else:
        db.session.delete(settings)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully deleted the settings!'
        }
        return response_object, 200


def update_settings(id, data):
    settings = Settings.query.filter_by(user_public_id=id).first()
    is_updated = False
    errors = {}

    # Check if ID is valid or not
    if not settings:
        errors['id'] = ["Setting ID does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Can not update settings!",
            'errors': errors
        }
        return response_object, 200
    else:
        # Check null
        if data['full_name'] == "":
            errors['full_name'] = ["Full name must not be null!"]

        if data['email'] == "":
            errors['email'] = ["Email must not be null!"]

        if data['phone_number'] == "":
            errors['phone_number'] = ["Phone number must not be null!"]

        if data['fax_number'] == "":
            errors['fax_number'] = ["Fax number must not be null!"]

        if data['address'] == "":
            errors['address'] = ["Address must not be null!"]

        if data['billing_address'] == "":
            errors['billing_address'] = ["Billing address must not be null!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update settings!",
                'errors': errors
            }
            return response_object, 200
        else:
            if data['full_name'] != settings.full_name:
                is_updated = True
                settings.full_name = data['full_name']

            if data['email'] != settings.email:
                is_updated = True
                settings.email = data['email']

            if data['phone_number'] != settings.phone_number:
                is_updated = True
                settings.phone_number = data['phone_number']

            if data['fax_number'] != settings.fax_number:
                is_updated = True
                settings.fax_number = data['fax_number']

            if data['address'] != settings.address:
                is_updated = True
                settings.address = data['address']

            if data['billing_address'] != settings.billing_address:
                is_updated = True
                settings.full_name = data['billing_address']

            if is_updated is True:
                settings.updated_on = datetime.datetime.utcnow()
                db.session.commit()

            settings_data = {}
            settings_data['id'] = str(settings.id)
            settings_data['full_name'] = settings.full_name
            settings_data['email'] = settings.email
            settings_data['phone_number'] = settings.phone_number
            settings_data['fax_number'] = settings.fax_number
            settings_data['address'] = settings.address
            settings_data['billing_address'] = settings.billing_address

            response_object = {
                'status': 'SUCCESS',
                'message': 'Successfully updated settings!',
                'data': settings_data
            }
            return response_object, 200

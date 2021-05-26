import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.model.setting import Settings


def is_admin(input_data):
    if input_data and input_data == 1:
        return 1

    return 0


def gender(input_data):
    if input_data == 0:
        return "Nam"

    return "Nữ"


def admin_response(input_data):
    if input_data == 1:
        return "Nhân viên"

    return "Quản trị viên"


def gender_response(input_data):
    if input_data and input_data == 1:
        return "Nam"
    else:
        return "Nữ"


def save_user(data):
    user = User.query.filter_by(username=data['username']).first()

    if user == None:
        id = str(uuid.uuid4())

        new_user = User(
            public_id=id,
            email=data['email'],
            phone_number=data['phone_number'],
            full_name=data['full_name'],
            gender=gender(data['gender']['value']),
            date_of_birth=datetime.datetime.strptime(
                data['date_of_birth'], '%Y-%m-%d'),
            avatar=data['avatar'],
            username=data['username'],
            password=data['password'],
            admin=is_admin(data['role']['value']),
            address=data['address'],
            created_on=datetime.datetime.utcnow(),
            updated_on=datetime.datetime.utcnow(),
        )
        save_changes(new_user)

        new_settings = Settings(
            full_name='CỬA HÀNG TIỆN LỢI MINISTOP',
            email='info@ministop.vn',
            phone_number='02835106870',
            fax_number='02835106871',
            address='215 Điện Biên Phủ, Phường 15, Quận Bình Thạnh, Tp.HCM',
            user_public_id=id,
            billing_address='Thành phố Hồ Chí Minh',
            created_on=datetime.datetime.utcnow(),
            updated_on=datetime.datetime.utcnow()
        )

        save_changes(new_settings)

        response_object = {
            'status': 'SUCCESS',
            'message': 'Create a new user successfully!',
        }

        return response_object, 200
    else:
        response_object = {
            'status': 'FAILED',
            'message': 'User already exists. Please log in!',
        }
        return response_object, 200


def get_all_users():
    all_users = User.query.all()
    output = []

    for user in all_users:
        auth_token = User.encode_auth_token(user.id)

        user_data = {}
        user_data['id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['token'] = auth_token.decode()
        user_data['phone_number'] = user.phone_number
        user_data['full_name'] = user.full_name
        user_data['avatar'] = user.avatar
        user_data['date_of_birth'] = str(user.date_of_birth).split(' ')[0]
        user_data['gender'] = {
            'value': 0 if user.gender == False else 1,
            'label': gender_response(user.gender)
        }
        user_data['role'] = {
            'value': 0 if user.admin == True else 0,
            'label': admin_response(user.admin)
        }
        user_data['address'] = user.address
        user_data['created_on'] = str(user.created_on)
        user_data['updated_on'] = str(user.updated_on)

        output.append(user_data)

    data = {}
    data['users'] = output

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of all users',
        'data': data
    }
    return response_object, 200


def get_user(public_id):
    errors = {}
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        errors['public_id'] = ['User ID does not exist!']
        response_object = {
            'status': 'FAILED',
            'message': "Can not get user data!",
            'errors': errors
        }
        return response_object, 200

    user_data = {}
    user_data['id'] = user.public_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['phone_number'] = user.phone_number
    user_data['full_name'] = user.full_name
    user_data['avatar'] = user.avatar
    user_data['date_of_birth'] = str(user.date_of_birth).split(' ')[0]
    user_data['gender'] = {
        'value': 0 if user.gender == False else 1,
        'label': gender_response(user.gender)
    }
    user_data['role'] = {
        'value': 0 if user.admin == True else 0,
        'label': admin_response(user.admin)
    }
    user_data['address'] = user.address
    user_data['created_on'] = str(user.created_on)
    user_data['updated_on'] = str(user.updated_on)

    response_object = {
        'status': 'SUCCESS',
        'message':  'Sucessfully getting information of user',
        'data': user_data
    }
    return response_object, 200


def generate_token(user):
    try:
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'Success',
            'message': 'Successfully registered!',
            'token': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'Fail',
            'message': 'Some error occurred. Please try again!'
        }
        return response_object, 401


def update_user_password(id, data, args):
    errors = {}
    user = User.query.filter_by(public_id=id).first()

    if not user:
        errors['id'] = ["User does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Failed to update user's password!",
            'errors': errors
        }
        return response_object, 200
    else:
        if data['old_password'] == "":
            errors['old_password'] = ["User's old password must not be null!"]

        if data['new_password'] == "":
            errors['new_password'] = ["User's new password must not be null!"]

        if data['confirmation_password'] == "":
            errors['confirmation_password'] = [
                "User's confirmation password must not be null!"]

        old_password = data['old_password']
        new_password = data['new_password']
        confirmation_password = data['confirmation_password']

        if user.check_password(old_password):
            if 'old_password' in errors.keys():
                errors['old_password'].append("Old password does not match!")
            else:
                errors['old_password'] = ["Old password does not match!"]

        if confirmation_password != new_password:
            if 'confirmation_password' in errors.keys():
                errors['confirmation_password'].append(
                    "Confirmation password does not match!")
            else:
                errors['confirmation_password'] = [
                    "Confirmation password does not match!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update user's password!",
                'errors': errors
            }
            return response_object, 200
        else:
            user.password = new_password
            user.updated_on = datetime.datetime.utcnow()
            db.session.commit()

            response_object = {
                'status': 'SUCCESS',
                'message': "Successfully update user's password!",
                'errors': errors
            }
            return response_object, 200


def update_user_profile(id, data, args):
    user = User.query.filter_by(public_id=id).first()
    is_updated = False
    errors = {}

    if not user:
        errors['id'] = ["User does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Failed to update user's password!",
            'errors': errors
        }
        return response_object, 200
    else:
        if data['email'] == '':
            errors['email'] = ["Email must not be null!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update user's information!",
                'errors': errors
            }
            return response_object, 200
        else:
            if data['email'] != user.email:
                # Check if supplier name is existed or not
                updated_user = User.query.filter_by(
                    email=data['email']).first()

                if updated_supplier:
                    errors['name'] = ["Email is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update user's information!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    user.email = data['email']
            else:
                if data['full_name'] != user.full_name:
                    is_updated = True
                    user.description = data['full_name']

                if data['phone_number'] != user.phone_number:
                    is_updated = True
                    user.phone_number = data['phone_number']

                if data['avatar'] != user.avatar:
                    is_updated = True
                    user.avatar = data['avatar']

                if data['date_of_birth'] != user.date_of_birth:
                    is_updated = True
                    user.date_of_birth = data['date_of_birth']

                if data['gender'] != user.gender:
                    is_updated = True
                    user.gender = int(data['gender']['value'])

                # if data['role'] != user.role:
                #     is_updated = True
                #     user.role = int(data['role']['value'])

                if data['address'] != user.address:
                    is_updated = True
                    user.address = data['address']

                if is_updated is True:
                    user.updated_on = datetime.datetime.utcnow()
                    db.session.commit()

                response_object = {
                    'status': 'SUCCESS',
                    'message': "Successfully updated user's information!",
                }

                return response_object, 200


def update_user(id, data, args):
    user = User.query.filter_by(public_id=id).first()
    is_updated = False
    errors = {}

    if not user:
        errors['id'] = ["User does not exist!"]
        response_object = {
            'status': 'FAILED',
            'message': "Failed to update user's password!",
            'errors': errors
        }
        return response_object, 200
    else:
        if data['email'] == '':
            errors['email'] = ["Email must not be null!"]

        if (len(errors) > 0):
            response_object = {
                'status': 'FAILED',
                'message': "Can not update user's information!",
                'errors': errors
            }
            return response_object, 200
        else:
            if data['email'] != user.email:
                # Check if supplier name is existed or not
                updated_user = User.query.filter_by(
                    email=data['email']).first()

                if updated_supplier:
                    errors['name'] = ["Email is already existed!"]
                    response_object = {
                        'status': 'FAILED',
                        'message': "Can not update user's information!",
                        'errors': errors
                    }
                    return response_object, 200
                else:
                    is_updated = True
                    user.email = data['email']
            else:
                role = int(data['role']['value'])
                is_admin = True if role == 0 else False

                if data['full_name'] != user.full_name:
                    is_updated = True
                    user.description = data['full_name']

                if data['phone_number'] != user.phone_number:
                    is_updated = True
                    user.phone_number = data['phone_number']

                if data['avatar'] != user.avatar:
                    is_updated = True
                    user.avatar = data['avatar']

                if data['date_of_birth'] != user.date_of_birth:
                    is_updated = True
                    user.date_of_birth = data['date_of_birth']

                if data['gender'] != user.gender:
                    is_updated = True
                    user.gender = int(data['gender']['value'])

                if is_admin != user.admin:
                    is_updated = True
                    user.admin = is_admin

                if data['address'] != user.address:
                    is_updated = True
                    user.address = data['address']

                if is_updated is True:
                    user.updated_on = datetime.datetime.utcnow()
                    db.session.commit()

                response_object = {
                    'status': 'SUCCESS',
                    'message': "Successfully updated user's information!",
                }

                return response_object, 200


def delete_user(id, args):
    errors = {}
    user = User.query.filter_by(public_id=id).first()

    if not user:
        respone_object = {
            'status': 'FAILED',
            'message': 'Can not delete user!',
            'errors': errors
        }
        return respone_object, 200
    else:
        db.session.delete(unit)
        db.session.commit()

        response_object = {
            'status': 'SUCCESS',
            'message': 'Successfully delete user!'
        }
        return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()

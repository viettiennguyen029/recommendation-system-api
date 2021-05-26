from app.main.model.user import User
from ..service.blacklist_service import save_token


class Auth:
    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(username=data['username']).first()

            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)

                if auth_token:
                    response_object = {
                        'status': 'SUCCESS',
                        'message': 'Successfully logged in!',
                        'data': {
                            'token': auth_token.decode(),
                            'user': user.get_data()
                        }
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'ERROR',
                    'message': 'Username or password does not match!'
                }
                return response_object, 200

        except Exception as e:
            print(e)
            response_object = {
                'status': 'ERROR',
                'message': 'Try again!'
            }
            return response_object, 200

    @staticmethod
    def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'ERROR',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'ERROR',
                'message': 'Provide a valid auth token!'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'SUCCESS',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,
                        'admin': user.admin
                        # 'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'ERROR',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'ERROR',
                'message': 'Provide a valid auth token!'
            }
            return response_object, 401

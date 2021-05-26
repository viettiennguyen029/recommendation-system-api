from flask import request
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..service.user_service import save_user, get_all_users, get_user, update_user, update_user_password, update_user_profile, delete_user

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('List all registered users')
    # @admin_token_required
    # @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    # @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('Create a new user')
    def post(self):
        """Create a new user """
        data = request.json
        return save_user(data=data)


@api.route('/change-password/<public_id>')
@api.param('public_id', 'The user identifier')
class ProfilePassword(Resource):
    @api.doc("Update a user's password")
    def put(self, public_id):
        """Update a user's password"""
        data = request.json
        args = request.args

        return update_user_password(public_id, data, args)


@api.route('/profile/<public_id>')
@api.param('public_id', 'The user identifier')
class ProfileInformation(Resource):
    @api.doc("Update a user's password")
    def put(self, public_id):
        """Update a user's password"""
        data = request.json
        args = request.args

        return update_user_profile(public_id, data, args)


@api.route('/<public_id>')
@api.param('public_id', 'The user identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('Get a user')
    # @api.marshal_with(_user)
    def get(self, public_id):
        """Get a user with a given identifier"""
        return get_user(public_id)

    @api.doc('Update a user with a given id')
    def put(self, public_id):
        """Update a user with a given id"""
        data = request.json
        args = request.args

        return update_user(public_id, data, args)

    @api.doc('Delete a user with a given id')
    def delete(self, public_id):
        """Delete a user"""
        args = request.args

        return delete_user(public_id, args)

from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Auth.UserManager import UserManager, User_auth

class UserAuthRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

    # Handles users logging in.
    def post(self):
        data = UserAuthRoute.parser.parse_args()
        with UserManager(data['email']) as usermanager:
            result = usermanager.login(data['password'])
        if result:
            return make_response(jsonify({'token': result}), HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Username or Password is wrong')


    # Deletes user from db
    @User_auth.login_required
    def delete(self):
        with UserManager(User_auth.current_user()) as usermanager:
            result = usermanager.delete()
        if result:
            return make_response(jsonify({'message': 'Account deleted'}), HTTPStatus.OK)
        abort(HTTPStatus.NOT_ACCEPTABLE, 'Could not delete account')

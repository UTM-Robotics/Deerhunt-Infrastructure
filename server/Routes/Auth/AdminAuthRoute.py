from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Auth.AdminManager import AdminManager


class AdminAuthRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

    # Handles post request for admin login
    def post(self):
        data = AdminAuthRoute.parser.parse_args()
        with AdminManager(data['username']) as adminmanager:
            result = adminmanager.login(data['password'])
        if result:
            return make_response(jsonify({'token': result}), HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'User does not exist or password is wrong')

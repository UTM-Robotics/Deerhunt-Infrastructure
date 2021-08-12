from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from server.Managers.Auth.AdminManager import AdminManager
from server.Managers.Auth.UserManager import auth


class AdminUserRoute(Resource):

    # Handles post request for admin login
    def post(self):
        with AdminManager(request.json['username']) as adminmanager:
            result = adminmanager.login(request.json['password'])
        if result:
            return make_response(jsonify({'token': result}), HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'User does not exist or password is wrong')

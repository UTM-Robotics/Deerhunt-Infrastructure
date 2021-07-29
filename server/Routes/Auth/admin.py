from http import HTTPStatus
from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from server.Managers.AdminManager import AdminManager

from server.Managers.UserManager import auth


class AdminRoute(Resource):
    def post(self):
        '''
        Handles post request for admin login
        '''
        with AdminManager(request.json['username']) as adminmanager:
            result = adminmanager.login(request.json['password'])
        if result:
            return make_response(jsonify({'token': result}), HTTPStatus.OK)
        abort(HTTPStatus.NOT_FOUND, 'User does not exist or password is wrong')

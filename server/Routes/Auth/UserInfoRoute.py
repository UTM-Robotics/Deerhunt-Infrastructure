from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Auth.UserManager import UserManager, User_auth
from server.Models.User import AdminUser, GeneralUser


class UserInfoRoute(Resource):

    # gets user info
    @User_auth.login_required
    def get(self):
        with UserManager(User_auth.current_user()) as usermanager:
            result = usermanager.find_user()
        if result:
            return make_response(jsonify({'email': result.get('email', '')}), HTTPStatus.OK)
        abort(HTTPStatus.NOT_ACCEPTABLE, 'Could not find info')

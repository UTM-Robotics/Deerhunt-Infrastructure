from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Auth.UserManager import UserManager, is_allowed, User_auth


class AmIAuthRoute(Resource):

    # Allow you in if you are authenticated
    @User_auth.login_required
    def get(self):
        print('auth works')
        return make_response('you are authenticated')



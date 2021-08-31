from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource

from server.Managers.Auth.UserManager import UserManager, User_auth

class UserRoute(Resource):

    # Handles users logging in.
    def post(self):
        with UserManager(request.json['email']) as usermanager:
            result = usermanager.login(request.json['password'])
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


class UserResetRoute(Resource):

    # Handles User password reset
    @User_auth.login_required
    def post(self):
        pass
        # with UserManager(auth.current_user()) as usermanager:
            # result = usermanager.

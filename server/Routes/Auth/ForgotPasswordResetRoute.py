from http import HTTPStatus

from flask import make_response, request, abort, jsonify, render_template
from flask_restful import Resource, reqparse
	
from server.Managers.Auth.UserManager import UserManager

class ForgotPasswordResetRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser()
    parser.add_argument('new_password', type=str, required=True, help='New password to change to')

    # Getting page for user to reset their password.
    def get(self, code):
        with UserManager(None, code) as usermanager:
            if usermanager.found:
                return make_response(render_template("reset.html", code=code))
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'You do not have access')

        
    def post(self, code):
        data = ForgotPasswordResetRoute.parser.parse_args()
        with UserManager(None,code) as usermanager:
            result = usermanager.update_password_forgotten(data['new_password'])
        if result:
            return make_response(jsonify({'message': 'Your password has been updated'}), 
                                HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Password could not be changed.')

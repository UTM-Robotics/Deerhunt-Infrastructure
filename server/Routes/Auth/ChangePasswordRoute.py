from http import HTTPStatus

from flask import make_response, abort, jsonify
from flask_restful import Resource, reqparse
	
from server.Managers.Auth.UserManager import User_auth, UserManager

class ChangePasswordRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser()
    parser.add_argument('old_password', type=str, required=True, help='Old user passwprd')
    parser.add_argument('new_password', type=str, required=True, help='New password to change to')

    @User_auth.login_required
    def post(self):
        data = ChangePasswordRoute.parser.parse_args()
        email = User_auth.current_user()
        with UserManager(email) as usermanager:
            result = usermanager.update_password(data['old_password'], data['new_password'])
        if result:
            return make_response(jsonify({'message': 'Your password has been updated'}), 
                                HTTPStatus.OK)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Password could not be changed.')
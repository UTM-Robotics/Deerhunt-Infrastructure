from http import HTTPStatus

from flask import make_response, request, abort, jsonify, render_template
from flask_restful import Resource, reqparse
	
from server.Managers.Auth.UserManager import CODE_LENGTH, UserManager

class ForgotPasswordRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email of user that forgot their password')

    # Handles post request for user registration.
    def post(self):
        data = ForgotPasswordRoute.parser.parse_args()
        print("1")
        with UserManager(data['email']) as usermanager:
            print(usermanager.found)
            if usermanager.found:

                usermanager.generate_code(CODE_LENGTH)
                result = usermanager.send_email('forgotpassword')
                usermanager.commit()
                print("2")
        if result:
            print("3")
            
            return make_response(jsonify({'message': 'Email with password reset link sent'}), 
                                HTTPStatus.OK)
        print(result)
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, 'Could not send password reset link')

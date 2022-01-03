from http import HTTPStatus
from datetime import time

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Auth.UserManager import UserManager, is_allowed


class UserTeamsRoute(Resource):

    # flask parser
    parser = reqparse.RequestParser(bundle_errors=False)
    parser.add_argument(
        "event_id", type=str, required=True, help="This field cannot be left blank"
    )

    # Handles post request for user registration.
    def post(self):
        data = UserRoute.parser.parse_args()
        if is_allowed(data["email"]):
            with UserManager(data["email"]) as usermanager:
                result = usermanager.register(data["password"])
            if result:
                return make_response(
                    jsonify(
                        {
                            "message": "Account partially created. Verification email sent\n"
                        }
                    ),
                    HTTPStatus.OK,
                )
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, "User already exists")

        abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Invalid email")

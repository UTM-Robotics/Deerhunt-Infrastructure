from flask_restful import Api, Resource
from flask import make_response, request
from http import HTTPStatus
from .emailbot import EmailBot


class RegisterRoute(Resource):
    def post(self):
        print(request.values)
        # result = database.users.find_one({'username': u})
        # with EmailBot() as email:
            # email.send_register()
        return make_response("Post works\n", HTTPStatus.OK)

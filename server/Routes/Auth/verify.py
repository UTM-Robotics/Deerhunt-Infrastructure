from flask_restful import Resource
from flask import make_response, abort, jsonify
from http import HTTPStatus

from server.Managers.UserManager import UserManager

class VerifyRoute(Resource):
    def get(self, code):
        with UserManager(None, code.strip('\n')) as usermanager:
            result = usermanager.verify_code()
        if result:
            return make_response(jsonify({'token': result}), 201)
        abort(HTTPStatus.GONE, 'Verification link expired or did not work for other reasons')

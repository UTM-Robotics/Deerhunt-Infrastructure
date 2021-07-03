from flask_restful import Resource
from flask import make_response, abort
from http import HTTPStatus

from server.Managers.UserManager import UserManager

class VerifyRoute(Resource):
    def post(self, code):
        with UserManager(None, code) as usermanager:
            result = usermanager.verify_code()
        if result:
            return make_response('Account verified!\n', HTTPStatus.CREATED) # need to add jwt token
        abort(HTTPStatus.GONE, 'Verification link expired or did not work for other reasons')

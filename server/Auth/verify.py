from flask_restful import Api, Resource
from flask import make_response, abort
from http import HTTPStatus

from ..config import Configuration


class VerifyRoute(Resource):
    def post(self, code):
        result = Configuration.Mongo.verify_code(code)
        if result:
            abort(410, 'Verification link expired or did not work for other reasons')
        return make_response('Account verified!\n', HTTPStatus.OK)
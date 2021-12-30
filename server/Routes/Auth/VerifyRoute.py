from http import HTTPStatus
from flask import make_response, abort, jsonify, render_template
from flask_restful import Resource

from server.Managers.Auth.UserManager import UserManager
from server.config import Configuration


class VerifyRoute(Resource):

    # get request when user clicks on verification link.
    def get(self, code):
        with UserManager(None, code.strip('\n')) as usermanager:
            result = usermanager.verify_code()
        if result:
            return make_response(render_template("verified.html", origin=Configuration.FLASK_ADDR))
        abort(HTTPStatus.GONE, 'Verification link expired or did not work for other reasons')

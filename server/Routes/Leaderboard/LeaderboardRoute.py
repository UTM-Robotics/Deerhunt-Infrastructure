from http import HTTPStatus

from flask import make_response, request, abort, jsonify
from flask_restful import Resource, reqparse

from server.Managers.Events.AdminEvents import EventsManager

class LeaderboardRoute(Resource):

    # flask parser for post request
    parser = reqparse.RequestParser()
    parser.add_argument('event', type=str, required=True, help='This field cannot be left blank')

    def get(self):
        data = LeaderboardRoute.parser.parse_args()
        


    def post(self):
        pass

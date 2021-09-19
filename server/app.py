from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Importing Auth routes
from server.Routes.Auth.register import RegisterRoute
from server.Routes.Auth.UserRoute import UserRoute
from server.Routes.Auth.verify import VerifyRoute
from server.Routes.Auth.AdminUserRoute import AdminUserRoute

from server.Routes.Events.Events import EventRoute
from server.Routes.Teams.Teams import TeamsRoute


app = Flask(__name__)
CORS(app)
api = Api(app)

# Initializing user auth routes
api.add_resource(RegisterRoute, '/api/register')
api.add_resource(VerifyRoute, '/api/verify/<code>')
api.add_resource(UserRoute, '/api/login')
api.add_resource(AdminUserRoute, '/api/adminlogin')

# Initializing other routes
api.add_resource(EventRoute, '/api/events')
api.add_resource(TeamsRoute, '/api/teams')

if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Importing Auth routes
from server.Routes.Auth.register import RegisterRoute
from server.Routes.Auth.UserRoute import UserRoute
from server.Routes.Auth.verify import VerifyRoute
from server.Routes.Auth.AdminUserRoute import AdminUserRoute

from server.Routes.Events.adminevent import AdminEventRoute


app = Flask(__name__)
CORS(app)
api = Api(app)

# Initializing
api.add_resource(RegisterRoute, '/api/register')
api.add_resource(VerifyRoute, '/api/verify/<code>')
api.add_resource(UserRoute, '/api/login')
api.add_resource(AdminUserRoute, '/api/adminlogin')

api.add_resource(AdminEventRoute, '/api/adminevent')

if __name__ == '__main__':
    app.run()

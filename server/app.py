from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from server.Routes.Auth.register import RegisterRoute
from server.Routes.Auth.login import LoginRoute
from server.Routes.Auth.verify import VerifyRoute
from server.Routes.Auth.admin import AdminRoute

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(RegisterRoute, '/register')
api.add_resource(VerifyRoute, '/verify/<code>')
api.add_resource(LoginRoute, '/login')
api.add_resource(AdminRoute, '/admin')


if __name__ == '__main__':
    app.run()

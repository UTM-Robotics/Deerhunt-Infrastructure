from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Importing Auth routes
from server.Routes.Auth.AmIAuthRoute import AmIAuthRoute
from server.Routes.Auth.UserRoute import UserRoute
from server.Routes.Auth.UserAuthRoute import UserAuthRoute
from server.Routes.Auth.VerifyRoute import VerifyRoute
from server.Routes.Auth.ChangePasswordRoute import ChangePasswordRoute
from server.Routes.Auth.ForgotPasswordRoute import ForgotPasswordRoute
from server.Routes.Auth.ForgotPasswordResetRoute import ForgotPasswordResetRoute
from server.Routes.Auth.AdminAuthRoute import AdminAuthRoute

from server.Routes.Events.Events import EventRoute
from server.Routes.Teams.Teams import TeamsRoute

app = Flask(__name__)
CORS(app)
api = Api(app)

# Initializing user auth routes
api.add_resource(UserRoute, '/api/user')
api.add_resource(UserAuthRoute, '/api/user/auth')
api.add_resource(VerifyRoute, '/api/user/verify/<code>')
api.add_resource(ChangePasswordRoute, '/api/user/changepassword')
api.add_resource(ForgotPasswordRoute, '/api/user/forgotpassword')
api.add_resource(ForgotPasswordResetRoute, '/api/user/forgotpassword/<code>')
api.add_resource(AdminAuthRoute, '/api/admin/auth')
api.add_resource(AmIAuthRoute, '/api/amiauth')

# Initializing other routes
api.add_resource(EventRoute, '/api/events')
api.add_resource(TeamsRoute, '/api/teams')
app.debug=True

if __name__ == '__main__':
    app.run()

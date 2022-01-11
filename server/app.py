from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Importing Auth routes
from server.Routes.Auth.UserTeamRoute import UserTeamRoute
from server.Routes.Teams.AddTeam import AddTeam
from server.Routes.Auth.AmIAuthRoute import AmIAuthRoute
from server.Routes.Auth.UserInfoRoute import UserInfoRoute
from server.Routes.Auth.UserRoute import UserRoute
from server.Routes.Auth.UserAuthRoute import UserAuthRoute
from server.Routes.Auth.VerifyRoute import VerifyRoute
from server.Routes.Auth.ChangePasswordRoute import ChangePasswordRoute
from server.Routes.Auth.ForgotPasswordRoute import ForgotPasswordRoute
from server.Routes.Auth.ForgotPasswordResetRoute import ForgotPasswordResetRoute
from server.Routes.Auth.AdminAuthRoute import AdminAuthRoute

from server.Routes.Events.Events import EventRoute
from server.Routes.Match.Match import MatchRoute
from server.Routes.Submissions.Submissions import SubmissionsRoute
from server.Routes.Teams.Team import TeamRoute
from server.Routes.Teams.Teams import TeamsRoute
from server.Routes.Leaderboard.LeaderboardRoute import LeaderboardRoute

from server.Routes.Consumer.Consumer import ConsumerRoute
from server.Routes.Consumer.ConsumerDownload import ConsumerDownloadRoute
from server.Routes.Match.MatchDownload import MatchDownloadRoute
app = Flask(__name__)
CORS(app)
api = Api(app)

# cap on max content length
# this is used mainly for submissions but also stops bad actors
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Initializing user auth routes
api.add_resource(UserRoute, "/api/user")
api.add_resource(UserAuthRoute, "/api/user/auth")
api.add_resource(VerifyRoute, "/api/user/verify/<code>")
api.add_resource(ChangePasswordRoute, "/api/user/changepassword")
api.add_resource(ForgotPasswordRoute, "/api/user/forgotpassword")
api.add_resource(ForgotPasswordResetRoute, "/api/user/forgotpassword/<code>")
api.add_resource(AdminAuthRoute, "/api/admin/auth")
api.add_resource(AmIAuthRoute, "/api/amiauth")
api.add_resource(UserInfoRoute, "/api/user/info")
api.add_resource(UserTeamRoute, "/api/user/team")

# Initializing other routes
api.add_resource(ConsumerRoute, '/api/requests')
api.add_resource(ConsumerDownloadRoute, '/api/consumer/downloads')

api.add_resource(MatchRoute, '/api/match')
api.add_resource(MatchDownloadRoute, '/api/match/download')
api.add_resource(EventRoute, "/api/events")
api.add_resource(TeamsRoute, "/api/teams")
api.add_resource(AddTeam, "/api/addmember")
api.add_resource(TeamRoute, "/api/team")
api.add_resource(SubmissionsRoute, "/api/submissions")
api.add_resource(LeaderboardRoute, "/api/leaderboard")


if __name__ == "__main__":
    app.run()

from .config import Configuration

from flask import Flask
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)


if __name__ == '__main__':
    app.run()
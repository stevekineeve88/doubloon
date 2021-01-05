from flask import \
    Flask
from flask_cors import CORS

from routes.api.v1.admin_user import admin_user_api
from routes.api.v1.app import app_api
from routes.api.v1.auth import auth_api
from routes.api.v1.basic_user import basic_user_api
from routes.api.v1.super_user import super_user_api
from routes.api.v1.utils import utils_api

app = Flask(__name__)
app.secret_key = "Flask Session String"
CORS(app, resources={r'/*': {"origins": "*"}})

app.register_blueprint(app_api)
app.register_blueprint(auth_api)
app.register_blueprint(super_user_api)
app.register_blueprint(admin_user_api)
app.register_blueprint(basic_user_api)
app.register_blueprint(utils_api)


@app.route("/")
def index():
    return "Hello"

import json

from flask import Blueprint, jsonify, request

from modules.App.managers.AppManager import AppManager
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.objects.AppUser import AppUser
from modules.User.objects.SystemRole import SystemRole
from routes.middleware import superware

app_api = Blueprint('app_api', __name__)


@app_api.route("/api/v1/app/create", methods=["POST"])
def app_create():
    try:
        app_manager = AppManager()
        app_user_manager = AppUserManager()
        system_role_manager = SystemRoleManager()

        post = json.loads(request.data.decode())
        user_post = post["user"]

        admin_role = system_role_manager.get_all().ADMIN
        app = app_manager.create(post["name"])
        user = AppUser()
        user.set_first_name(user_post["first_name"])
        user.set_last_name(user_post["last_name"])
        user.set_email(user_post["email"])
        user.set_password(user_post["password"])
        user.set_username(user_post["username"])
        user.set_phone(user_post["phone"])
        user.set_system_role(SystemRole(admin_role["id"], admin_role["const"], admin_role["description"]))
        app_user = app_user_manager.create(app, user)
        return jsonify({
            "success": True,
            "results": app_user.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@app_api.route("/api/v1/app/search", methods=["GET"])
@superware.superware()
def app_search():
    return jsonify({
        "test": "Hello two"
    })

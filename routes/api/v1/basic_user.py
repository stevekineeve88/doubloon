import json
from flask import Blueprint, jsonify, request

from modules.App.managers.AppManager import AppManager
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.objects.AppUser import AppUser
from modules.User.objects.SystemRole import SystemRole
from routes.middleware.appselfware import appselfware

basic_user_api = Blueprint('basic_user_api', __name__)


@basic_user_api.route("/api/v1/user/app/create", methods=["POST"])
def create_app_user():
    try:
        app_user_manager = AppUserManager()
        system_role_manager = SystemRoleManager()
        app_manager = AppManager()
        app_uuid = request.headers.get("app_access_id") or ""
        app_api_key = request.headers.get("app_api_key") or ""
        post = json.loads(request.data.decode())
        app = app_manager.get_by_uuid(app_uuid)
        if app_api_key != app.get_api_key():
            raise Exception("Failed to authenticate")
        system_roles = system_role_manager.get_all()
        user_role = system_roles.USER
        system_role = SystemRole(user_role["id"], user_role["const"], user_role["description"])
        app_user = AppUser()
        app_user.set_system_role(system_role)
        app_user.set_username(post["username"])
        app_user.set_password(post["password"])
        app_user.set_email(post["email"])
        app_user.set_phone(post["phone"])
        app_user.set_first_name(post["first_name"])
        app_user.set_last_name(post["last_name"])
        app_user = app_user_manager.create(app, app_user)
        app_user_dict = app_user.to_dict()
        app_user_dict.pop("app")
        return jsonify({
            "success": True,
            "result": app_user_dict
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@basic_user_api.route("/api/v1/user/app/get/<app_user_id>", methods=["GET"])
@appselfware()
def get_app_user(app_user_id):
    try:
        app_user_manager = AppUserManager()
        user = app_user_manager.get(app_user_id)
        user_dict = user.to_dict()
        user_dict.pop("app")
        return jsonify({
            "success": True,
            "result": user_dict
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@basic_user_api.route("/api/v1/user/app/update/<app_user_id>", methods=["PATCH"])
@appselfware()
def update_app_user(app_user_id):
    try:
        app_user_manager = AppUserManager()
        post = json.loads(request.data.decode())
        user = app_user_manager.get(app_user_id)
        user.set_first_name(post["first_name"])
        user.set_last_name(post["last_name"])
        user.set_email(post["email"])
        user.set_phone(post["phone"])
        user = app_user_manager.update(user)
        return jsonify({
            "success": True,
            "result": {
                "first_name": user.get_first_name(),
                "last_name": user.get_last_name(),
                "email": user.get_email(),
                "phone": user.get_phone()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@basic_user_api.route("/api/v1/user/app/delete/<app_user_id>", methods=["DELETE"])
@appselfware()
def delete_app_user(app_user_id):
    try:
        app_user_manager = AppUserManager()
        user = app_user_manager.delete(app_user_id)
        return jsonify({
            "success": True,
            "result": {
                "id": user.get_id(),
                "user_status": user.get_user_status().to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@basic_user_api.route("/api/v1/user/app/disable/<app_user_id>", methods=["PATCH"])
@appselfware()
def disable_app_user(app_user_id):
    try:
        app_user_manager = AppUserManager()
        user = app_user_manager.disable(app_user_id)
        return jsonify({
            "success": True,
            "result": {
                "id": user.get_id(),
                "user_status": user.get_user_status().to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@basic_user_api.route("/api/v1/user/app/activate/<app_user_id>", methods=["PATCH"])
@appselfware()
def activate_app_user(app_user_id):
    try:
        app_user_manager = AppUserManager()
        user = app_user_manager.activate(app_user_id)
        return jsonify({
            "success": True,
            "result": {
                "id": user.get_id(),
                "user_status": user.get_user_status().to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@basic_user_api.route("/api/v1/user/app/update-password/<app_user_id>", methods=["PATCH"])
@appselfware()
def update_app_user_password(app_user_id):
    try:
        app_user_manager = AppUserManager()
        post = json.loads(request.data.decode())
        app_user_manager.update_password(app_user_id, post["old_password"], post["new_password"])
        return jsonify({
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

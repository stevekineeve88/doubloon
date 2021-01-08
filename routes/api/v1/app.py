import json

from flask import Blueprint, jsonify, request

from modules.App.managers.AppManager import AppManager
from modules.App.objects.App import App
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.objects.AppUser import AppUser
from modules.User.objects.SystemRole import SystemRole
from routes.middleware.admin_ware import admin_ware
from routes.middleware.super_ware import super_ware

app_api = Blueprint('app_api', __name__)


@app_api.route("/api/v1/app/create", methods=["POST"])
def create_app():
    """ API create app
    Returns:
        json
    """
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


@app_api.route("/api/v1/app/get", methods=["GET"])
@admin_ware()
def get_app():
    """ API get app
    Returns:
        json
    """
    try:
        app_manager = AppManager()
        app_uuid = request.headers.get("app_access_id") or ""
        app = app_manager.get_by_uuid(app_uuid)
        return jsonify({
            "success": True,
            "result": app.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@app_api.route("/api/v1/app/search", methods=["POST"])
@super_ware()
def search_apps():
    """ API get apps
    Returns:
        json
    """
    try:
        app_manager = AppManager()
        post = json.loads(request.data.decode())
        limit = post["limit"] if "limit" in post else 100
        limit = 100 if limit > 100 else limit
        result = app_manager.search(
            search=post["search"] if "search" in post else "",
            limit=limit,
            page=post["page"] if "page" in post else 1,
            order=post["order"] if "order" in post else {}
        )
        apps = result.get_data()
        app: App
        app_result = []
        for app in apps:
            app_result.append(app.to_dict())
        return jsonify({
            "success": True,
            "result": {
                "data": app_result,
                "meta": result.get_metadata()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

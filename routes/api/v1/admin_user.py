import json
from flask import Blueprint, jsonify, request

from modules.App.managers.AppManager import AppManager
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.objects.AppUser import AppUser
from modules.User.objects.SystemRole import SystemRole
from routes.middleware.admin_ware import admin_ware

admin_user_api = Blueprint('admin_user_api', __name__)


@admin_user_api.route("/api/v1/user/admin/create", methods=["POST"])
@admin_ware()
def create_app_user():
    """ API create app user
    Returns:
        json
    """
    try:
        app_user_manager = AppUserManager()
        system_role_manager = SystemRoleManager()
        app_manager = AppManager()
        app_uuid = request.headers.get("app_access_id") or ""
        post = json.loads(request.data.decode())
        app = app_manager.get_by_uuid(app_uuid)
        system_roles_datalist = system_role_manager.get_all()
        system_role_array = system_roles_datalist.get(post["system_role_id"])
        system_role = SystemRole(system_role_array["id"], system_role_array["const"], system_role_array["description"])
        app_user = AppUser()
        app_user.set_system_role(system_role)
        app_user.set_username(post["username"])
        app_user.set_password(post["password"])
        app_user.set_email(post["email"])
        app_user.set_phone(post["phone"])
        app_user.set_first_name(post["first_name"])
        app_user.set_last_name(post["last_name"])
        app_user = app_user_manager.create(app, app_user)
        return jsonify({
            "success": True,
            "result": app_user.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@admin_user_api.route("/api/v1/user/admin/search", methods=["POST"])
@admin_ware()
def get_app_users():
    """ API get app users
    Returns:
        json
    """
    try:
        app_user_manager = AppUserManager()
        app_manager = AppManager()
        post = json.loads(request.data.decode())
        limit = post["limit"] if "limit" in post else 100
        limit = 100 if limit > 100 else limit
        app_uuid = request.headers.get("app_access_id") or ""
        app = app_manager.get_by_uuid(app_uuid)
        result = app_user_manager.search_app_users(
            app,
            search=post["search"] if "search" in post else "",
            limit=limit,
            page=post["page"] if "page" in post else 1,
            user_status_id=post["user_status"] if "user_status" in post else None,
            order=post["order"] if "order" in post else {}
        )
        users = result.get_data()
        user: AppUser
        user_result = []
        for user in users:
            user_result.append(user.to_dict())
        return jsonify({
            "success": True,
            "result": {
                "data": user_result,
                "meta": result.get_metadata()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

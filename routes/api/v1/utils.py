from flask import Blueprint, jsonify, request
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.objects.SystemRole import SystemRole
from routes.middleware.admin_ware import admin_ware

utils_api = Blueprint('utils_api', __name__)


@utils_api.route("/api/v1/utils/system-roles", methods=["GET"])
@admin_ware()
def get_system_roles():
    """ API get system roles
    Returns:
        json
    """
    try:
        system_role_manager = SystemRoleManager()
        system_roles = system_role_manager.get_all().get_all()
        system_roles_array = []
        for key, system_role in system_roles.items():
            system_role_obj = SystemRole(system_role["id"], system_role["const"], system_role["description"])
            system_roles_array.append(system_role_obj.to_dict())
        return jsonify({
            "success": True,
            "result": system_roles_array
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

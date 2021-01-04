import json

from flask import Blueprint, jsonify, request

from modules.App.managers.AppManager import AppManager
from modules.Authentication.managers.AuthenticationManager import AuthenticationManager

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/api/v1/auth/super/login", methods=["POST"])
def super_login():
    try:
        post = json.loads(request.data.decode())
        auth_manager = AuthenticationManager()
        result = auth_manager.login_super(post["username"], post["password"])
        if not result.get_status():
            return jsonify({
                "success": False,
                "message": result.get_message()
            })
        return jsonify({
            "success": True,
            "results": {
                "token": result.get_metadata_attribute("token"),
                "user": result.get_data()[0].to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@auth_api.route("/api/v1/auth/admin/login", methods=["POST"])
def admin_login():
    try:
        post = json.loads(request.data.decode())
        auth_manager = AuthenticationManager()
        app_manager = AppManager()
        app = app_manager.get_by_name(post["app_name"])
        result = auth_manager.login_admin(post["username"], post["password"], app)
        if not result.get_status():
            return jsonify({
                "success": False,
                "message": result.get_message()
            })
        return jsonify({
            "success": True,
            "results": {
                "token": result.get_metadata_attribute("token"),
                "user": result.get_data()[0].to_dict()
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

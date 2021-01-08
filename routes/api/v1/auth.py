import json

from flask import Blueprint, jsonify, request

from modules.App.managers.AppManager import AppManager
from modules.Authentication.managers.AuthenticationManager import AuthenticationManager

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/api/v1/auth/super/login", methods=["POST"])
def super_login():
    """ API super user login
    Returns:
        json
    """
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
    """ API admin user login
    Returns:
        json
    """
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


@auth_api.route("/api/v1/auth/app/login", methods=["POST"])
def app_login():
    """ API app user login
    Returns:
        json
    """
    try:
        post = json.loads(request.data.decode())
        auth_manager = AuthenticationManager()
        app_manager = AppManager()
        app = app_manager.get_by_name(post["app_name"])
        result = auth_manager.login_app(post["username"], post["password"], app)
        if not result.get_status():
            return jsonify({
                "success": False,
                "message": result.get_message()
            })
        user_dict = result.get_data()[0].to_dict()
        user_dict.pop("app")
        return jsonify({
            "success": True,
            "results": {
                "token": result.get_metadata_attribute("token"),
                "user": user_dict
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

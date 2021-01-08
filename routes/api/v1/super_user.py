import json
from flask import Blueprint, jsonify, request
from modules.User.managers.SuperUserManager import SuperUserManager
from modules.User.objects.SuperUser import SuperUser
from routes.middleware.super_self_ware import super_self_ware
from routes.middleware.super_ware import super_ware

super_user_api = Blueprint('super_user_api', __name__)


@super_user_api.route("/api/v1/user/super/create", methods=["POST"])
@super_ware()
def create_super_user():
    """ API create super user
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        post = json.loads(request.data.decode())
        super_user = SuperUser()
        super_user.set_username(post["username"])
        super_user.set_password(post["password"])
        super_user.set_email(post["email"])
        super_user.set_phone(post["phone"])
        super_user.set_first_name(post["first_name"])
        super_user.set_last_name(post["last_name"])
        super_user = super_user_manager.create(super_user)
        return jsonify({
            "success": True,
            "result": super_user.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@super_user_api.route("/api/v1/user/super/get/<super_user_id>", methods=["GET"])
@super_ware()
def get_super_user(super_user_id):
    """ API get super user
    Args:
        (int) super_user_id: Super user ID
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        user = super_user_manager.get(super_user_id)
        return jsonify({
            "success": True,
            "result": user.to_dict()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


@super_user_api.route("/api/v1/user/super/delete/<super_user_id>", methods=["DELETE"])
@super_ware()
def delete_super_user(super_user_id):
    """ API delete super user
    Args:
        (int) super_user_id: Super user ID
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        user = super_user_manager.delete(super_user_id)
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


@super_user_api.route("/api/v1/user/super/disable/<super_user_id>", methods=["PATCH"])
@super_ware()
def disable_super_user(super_user_id):
    """ API disable super user
    Args:
        (int) super_user_id: Super user ID
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        user = super_user_manager.disable(super_user_id)
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


@super_user_api.route("/api/v1/user/super/activate/<super_user_id>", methods=["PATCH"])
@super_ware()
def activate_super_user(super_user_id):
    """ API activate super user
    Args:
        (int) super_user_id: Super user ID
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        user = super_user_manager.activate(super_user_id)
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


@super_user_api.route("/api/v1/user/super/list", methods=["POST"])
@super_ware()
def list_super_users():
    """ API list super users
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        post = json.loads(request.data.decode())
        limit = post["limit"] if "limit" in post else 100
        limit = 100 if limit > 100 else limit
        result = super_user_manager.search(
            search=post["search"] if "search" in post else "",
            limit=limit,
            page=post["page"] if "page" in post else 1,
            user_status_id=post["user_status"] if "user_status" in post else None,
            order=post["order"] if "order" in post else {}
        )
        users = result.get_data()
        user: SuperUser
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


@super_user_api.route("/api/v1/user/super/update/<super_user_id>", methods=["PATCH"])
@super_self_ware()
def update_super_user(super_user_id):
    """ API update super user
    Args:
        (int) super_user_id: Super user ID
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        post = json.loads(request.data.decode())
        user = super_user_manager.get(super_user_id)
        user.set_first_name(post["first_name"])
        user.set_last_name(post["last_name"])
        user.set_email(post["email"])
        user.set_phone(post["phone"])
        user = super_user_manager.update(user)
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


@super_user_api.route("/api/v1/user/super/update-password/<super_user_id>", methods=["PATCH"])
@super_self_ware()
def update_super_user_password(super_user_id):
    """ API update super user password
    Args:
        (int) super_user_id: Super user ID
    Returns:
        json
    """
    try:
        super_user_manager = SuperUserManager()
        post = json.loads(request.data.decode())
        super_user_manager.update_password(super_user_id, post["old_password"], post["new_password"])
        return jsonify({
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })

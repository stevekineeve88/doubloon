import json

from flask import Blueprint, jsonify, request

from modules.User.managers.SuperUserManager import SuperUserManager
from modules.User.objects.SuperUser import SuperUser
from routes.middleware.superware import superware

user_api = Blueprint('user_api', __name__)


@user_api.route("/api/v1/user/super/create", methods=["POST"])
@superware()
def create_super_user():
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


@user_api.route("/api/v1/user/super/list", methods=["POST"])
@superware()
def list_super_users():
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

from functools import wraps
from flask import jsonify, request
from routes.config.APIConfig import APIConfig


def superware():
    def _superware(f):
        @wraps(f)
        def __superware(*args, **kwargs):
            api_config = APIConfig()
            access_id = request.headers.get("access_id") or ""
            api_key = request.headers.get("api_key") or ""
            bearer_token = request.headers.get("Authorization") or ""
            if api_config.is_super_user_auth(access_id, api_key, bearer_token):
                return f(*args, **kwargs)
            return jsonify({
                "success": False,
                "message": "No Authorization"
            })
        return __superware
    return _superware

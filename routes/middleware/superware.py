from functools import wraps
from flask import jsonify, request, session

from modules.Authentication.managers.SessionManager import SessionManager
from modules.Util.APIConfig import APIConfig


def superware():
    def _superware(f):
        @wraps(f)
        def __superware(*args, **kwargs):
            session_manager = SessionManager()
            api_config = APIConfig()
            access_id = request.headers.get("access_id") or ""
            api_key = request.headers.get("api_key") or ""
            token = request.headers.get("token") or ""
            user_session = session_manager.get_super_token(token)
            if api_config.is_doubloon_access_id(access_id) and \
                    api_config.is_doubloon_api_key(api_key) and \
                    user_session is not None:
                return f(*args, **kwargs)
            return jsonify({
                "success": False,
                "message": "No Authorization"
            })
        return __superware
    return _superware

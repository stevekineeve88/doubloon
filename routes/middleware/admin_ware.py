from functools import wraps
from flask import jsonify, request
from routes.middleware.config.CheckpointBuilder import CheckpointBuilder
from routes.middleware.config.checkpoints.AdminCheckpoint import AdminCheckpoint
from routes.middleware.config.checkpoints.SuperCheckpoint import SuperCheckpoint


def admin_ware():
    """ Admin middleware
    Returns:
        json
    """
    def _admin_ware(f):
        @wraps(f)
        def __admin_ware(*args, **kwargs):
            access_id = request.headers.get("access_id") or ""
            api_key = request.headers.get("api_key") or ""
            bearer_token = request.headers.get("Authorization") or ""
            app_access_id = request.headers.get("app_access_id") or ""
            app_api_key = request.headers.get("app_api_key") or ""
            checkpoint_builder = CheckpointBuilder([
                SuperCheckpoint(access_id, api_key, bearer_token),
                AdminCheckpoint(app_access_id, app_api_key, bearer_token)
            ])
            if checkpoint_builder.passes():
                return f(*args, **kwargs)
            return jsonify({
                "success": False,
                "message": "No Authorization"
            })
        return __admin_ware
    return _admin_ware

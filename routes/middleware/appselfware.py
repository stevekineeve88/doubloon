from functools import wraps
from flask import jsonify, request
from routes.middleware.config.CheckpointBuilder import CheckpointBuilder
from routes.middleware.config.checkpoints.AdminCheckpoint import AdminCheckpoint
from routes.middleware.config.checkpoints.AppSelfCheckpoint import AppSelfCheckpoint
from routes.middleware.config.checkpoints.SuperCheckpoint import SuperCheckpoint


def appselfware():
    def _appselfware(f):
        @wraps(f)
        def __appselfware(*args, **kwargs):
            access_id = request.headers.get("access_id") or ""
            api_key = request.headers.get("api_key") or ""
            app_access_id = request.headers.get("app_access_id") or ""
            app_api_key = request.headers.get("app_api_key") or ""
            bearer_token = request.headers.get("Authorization") or ""
            checkpoint_builder = CheckpointBuilder([
                SuperCheckpoint(access_id, api_key, bearer_token),
                AdminCheckpoint(app_access_id, app_api_key, bearer_token),
                AppSelfCheckpoint(app_access_id, app_api_key, bearer_token, kwargs.get("app_user_id"))
            ])
            if checkpoint_builder.passes():
                return f(*args, **kwargs)
            return jsonify({
                "success": False,
                "message": "No Authorization"
            })
        return __appselfware
    return _appselfware

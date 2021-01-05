from functools import wraps
from flask import jsonify, request
from routes.middleware.config.CheckpointBuilder import CheckpointBuilder
from routes.middleware.config.checkpoints.SuperSelfCheckpoint import SuperSelfCheckpoint


def superselfware():
    def _superselfware(f):
        @wraps(f)
        def __superselfware(*args, **kwargs):
            access_id = request.headers.get("access_id") or ""
            api_key = request.headers.get("api_key") or ""
            bearer_token = request.headers.get("Authorization") or ""
            checkpoint_builder = CheckpointBuilder([
                SuperSelfCheckpoint(access_id, api_key, bearer_token, kwargs.get("super_user_id"))
            ])
            if checkpoint_builder.passes():
                return f(*args, **kwargs)
            return jsonify({
                "success": False,
                "message": "No Authorization"
            })
        return __superselfware
    return _superselfware

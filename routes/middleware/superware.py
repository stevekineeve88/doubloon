from functools import wraps
from flask import jsonify, request
from routes.middleware.config.CheckpointBuilder import CheckpointBuilder
from routes.middleware.config.checkpoints.SuperCheckpoint import SuperCheckpoint


def superware():
    def _superware(f):
        @wraps(f)
        def __superware(*args, **kwargs):
            access_id = request.headers.get("access_id") or ""
            api_key = request.headers.get("api_key") or ""
            bearer_token = request.headers.get("Authorization") or ""
            checkpoint_builder = CheckpointBuilder([
                SuperCheckpoint(access_id, api_key, bearer_token)
            ])
            if checkpoint_builder.passes():
                return f(*args, **kwargs)
            return jsonify({
                "success": False,
                "message": "No Authorization"
            })
        return __superware
    return _superware

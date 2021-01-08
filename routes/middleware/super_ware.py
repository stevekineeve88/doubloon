from functools import wraps
from flask import jsonify, request
from routes.middleware.config.CheckpointBuilder import CheckpointBuilder
from routes.middleware.config.checkpoints.SuperCheckpoint import SuperCheckpoint


def super_ware():
    """ Super middleware
    Returns:
        json
    """
    def _super_ware(f):
        @wraps(f)
        def __super_ware(*args, **kwargs):
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
        return __super_ware
    return _super_ware

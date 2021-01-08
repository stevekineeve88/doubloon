from functools import wraps
from flask import jsonify, request
from routes.middleware.config.CheckpointBuilder import CheckpointBuilder
from routes.middleware.config.checkpoints.SuperSelfCheckpoint import SuperSelfCheckpoint


def super_self_ware():
    """ Super self middleware
    Returns:
        json
    """
    def _super_self_ware(f):
        @wraps(f)
        def __super_self_ware(*args, **kwargs):
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
        return __super_self_ware
    return _super_self_ware

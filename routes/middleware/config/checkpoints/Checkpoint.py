import os

from modules.Authentication.managers.SessionManager import SessionManager


class Checkpoint:

    def __init__(self):
        self._doubloon_access_id = os.environ["DOUBLOON_ACCESS_ID"]
        self._doubloon_api_key = os.environ["DOUBLOON_API_KEY"]
        self._session_manager: SessionManager = SessionManager()

    def passes(self):
        pass

    def split_token(self, bearer_token: str) -> str:
        token_keys = bearer_token.split("Bearer ")
        token = ""
        if len(token_keys) == 2:
            token = token_keys[1]
        return token

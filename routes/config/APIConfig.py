import os

from modules.Authentication.managers.SessionManager import SessionManager


class APIConfig:
    def __init__(self):
        self.__doubloon_access_id = os.environ["DOUBLOON_ACCESS_ID"]
        self.__doubloon_api_key = os.environ["DOUBLOON_API_KEY"]

    def is_super_user_auth(self, access_id: str, api_key: str, bearer_token: str) -> bool:
        session_manager = SessionManager()
        token = self.__split_token(bearer_token)
        user_session = session_manager.get_super_token(token)
        return self.__doubloon_access_id == access_id and \
                self.__doubloon_api_key == api_key and \
                user_session is not None

    def __split_token(self, bearer_token: str) -> str:
        token_keys = bearer_token.split("Bearer ")
        token = ""
        if len(token_keys) == 2:
            token = token_keys[1]
        return token

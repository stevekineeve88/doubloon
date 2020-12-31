import os

from modules.Authentication.managers.SessionManager import SessionManager


class APIConfig:
    def __init__(self):
        self.__doubloon_access_id = os.environ["DOUBLOON_ACCESS_ID"]
        self.__doubloon_api_key = os.environ["DOUBLOON_API_KEY"]
        self.__session_manager: SessionManager = SessionManager()

    def is_super_user_auth(self, access_id: str, api_key: str, bearer_token: str) -> bool:
        token = self.split_token(bearer_token)
        user_session = self.__session_manager.get_super_token(token)
        return self.__doubloon_access_id == access_id and \
                self.__doubloon_api_key == api_key and \
                user_session is not None

    def is_super_user_logged_in(self, super_user_id: int, bearer_token: str) -> bool:
        token = self.split_token(bearer_token)
        user_session = self.__session_manager.get_super_token(token)
        if user_session is None:
            return False
        return int(super_user_id) == int(user_session["id"])


    def split_token(self, bearer_token: str) -> str:
        token_keys = bearer_token.split("Bearer ")
        token = ""
        if len(token_keys) == 2:
            token = token_keys[1]
        return token

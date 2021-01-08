import os

from modules.Authentication.managers.SessionManager import SessionManager


class Checkpoint:
    """ Base class for all checkpoint classes
    """

    def __init__(self):
        """ Constructor for Checkpoint
        """
        self._doubloon_access_id = os.environ["DOUBLOON_ACCESS_ID"]
        self._doubloon_api_key = os.environ["DOUBLOON_API_KEY"]
        self._session_manager: SessionManager = SessionManager()

    def passes(self) -> bool:
        """ Check if passes conditions for checkpoint
        Returns:
            bool
        """
        pass

    @classmethod
    def split_token(cls, bearer_token: str) -> str:
        """ Split Bearer token
        Args:
            (str) bearer_token: Token
        Returns:
            str
        """
        token_keys = bearer_token.split("Bearer ")
        token = ""
        if len(token_keys) == 2:
            token = token_keys[1]
        return token

from routes.middleware.config.checkpoints.Checkpoint import Checkpoint


class SuperSelfCheckpoint(Checkpoint):
    """ Class for super self login middleware checkpoint
    """

    def __init__(self, access_id: str, api_key: str, bearer_token: str, super_user_id: int):
        """ Constructor for SuperSelfCheckpoint
        Args:
            (str) access_id:        Super access UUID
            (str) api_key:          Super API key
            (str) bearer_token:     Super user token
            (int) super_user_id:    Super user ID
        """
        super().__init__()
        self.__access_id = access_id
        self.__api_key = api_key
        self.__bearer_token = bearer_token
        self.__super_user_id = super_user_id

    def passes(self) -> bool:
        """ Extends checkpoint passes
        Returns:
            bool
        """
        token = self.split_token(self.__bearer_token)
        user_session = self._session_manager.get_super_user_session(token)
        if user_session is None:
            return False
        return self._doubloon_access_id == self.__access_id and \
               self._doubloon_api_key == self.__api_key and \
               int(user_session["id"]) == int(self.__super_user_id)

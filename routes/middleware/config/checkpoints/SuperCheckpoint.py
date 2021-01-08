from routes.middleware.config.checkpoints.Checkpoint import Checkpoint


class SuperCheckpoint(Checkpoint):
    """ Class for super middleware checkpoint
    """

    def __init__(self, access_id: str, api_key: str, bearer_token: str):
        """ Constructor for SuperCheckpoint
        Args:
            (str) access_id:      Super access UUID
            (str) api_key:        Super API key
            (str) bearer_token:   Super user token
        """
        super().__init__()
        self.__access_id = access_id
        self.__api_key = api_key
        self.__bearer_token = bearer_token

    def passes(self) -> bool:
        """ Extends Checkpoint passes
        Returns:
            bool
        """
        token = self.split_token(self.__bearer_token)
        user_session = self._session_manager.get_super_user_session(token)
        return self._doubloon_access_id == self.__access_id and \
               self._doubloon_api_key == self.__api_key and \
               user_session is not None


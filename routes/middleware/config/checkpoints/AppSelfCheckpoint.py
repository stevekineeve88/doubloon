from routes.middleware.config.checkpoints.Checkpoint import Checkpoint


class AppSelfCheckpoint(Checkpoint):
    """ Class for app user self login checkpoint
    """

    def __init__(self, access_id: str, api_key: str, bearer_token: str, app_user_id: int):
        """ Constructor for AppSelfCheckpoint
        Args:
            (str) access_id:    App access UUID
            (str) api_key:      App API key
            (str) bearer_token: App user token
            (int) app_user_id:  App user ID
        """
        super().__init__()
        self.__access_id = access_id
        self.__api_key = api_key
        self.__bearer_token = bearer_token
        self.__app_user_id = app_user_id

    def passes(self) -> bool:
        """ Extends Checkpoint passes
        Returns:
            bool
        """
        token = self.split_token(self.__bearer_token)
        user_session = self._session_manager.get_app_user_session(self.__access_id, token)
        if user_session is None:
            return False
        return user_session["app"]["uuid"] == self.__access_id and \
               user_session["app"]["api_key"] == self.__api_key and \
               int(user_session["id"]) == int(self.__app_user_id)

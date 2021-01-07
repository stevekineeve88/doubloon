from routes.middleware.config.checkpoints.Checkpoint import Checkpoint


class AdminCheckpoint(Checkpoint):
    def __init__(self, access_id: str, api_key: str, bearer_token: str):
        super().__init__()
        self.__access_id = access_id
        self.__api_key = api_key
        self.__bearer_token = bearer_token

    def passes(self):
        token = self.split_token(self.__bearer_token)
        user_session = self._session_manager.get_admin_user_session(token)
        if user_session is None:
            return False
        return user_session["app"]["uuid"] == self.__access_id and \
               user_session["app"]["api_key"] == self.__api_key


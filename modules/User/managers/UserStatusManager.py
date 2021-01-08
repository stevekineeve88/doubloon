from modules.User.repositories.UserStatusRepo import UserStatusRepo
from modules.Util.DataList import DataList


class UserStatusManager:
    """ Manager for handling user status CRUD operations
    """

    def __init__(self, **kwargs):
        """ Constructor for UserStatusManager
        Args:
            **kwargs: Dependencies if needed
                (UserStatusRepo) user_status_repo
        """
        self.user_status_repo: UserStatusRepo = kwargs.get('user_status_repo') or UserStatusRepo()
        self.user_statuses = None

    def get_all(self) -> DataList:
        """ Get all user statuses
        Returns:
            DataList
        """
        if self.user_statuses is not None:
            return self.user_statuses
        result = self.user_status_repo.load_all()
        if not result.get_status():
            raise Exception("Could not load user statuses")
        self.user_statuses = DataList(result.get_data())
        return self.user_statuses

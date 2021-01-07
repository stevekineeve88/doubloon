from modules.User.objects.User import User


class SuperUser(User):
    """ Object that holds extended user attributes of super user
    """

    def __init__(self):
        """ Constructor for SuperUser
        """
        super().__init__()

    def to_dict(self) -> dict:
        """ Convert object to dictionary
        Returns:
            dict
        """
        return {
            "id": self.get_id(),
            "user_status": self.get_user_status().to_dict(),
            "uuid": self.get_uuid(),
            "username": self.get_username(),
            "first_name": self.get_first_name(),
            "last_name": self.get_last_name(),
            "email": self.get_email(),
            "phone": self.get_phone(),
            "created_date": self.get_created_date()
        }

from modules.App.objects.App import App
from modules.User.objects.SystemRole import SystemRole
from modules.User.objects.User import User


class AppUser(User):
    """ Object that holds extended user attributes for app user
    """

    def __init__(self):
        """ Constructor for AppUser
        """
        super().__init__()
        self.app = None
        self.system_role = None

    def set_app(self, app: App):
        """ Set app
        Args:
            (App) app: App to set
        """
        self.app = app

    def get_app(self) -> App:
        """ Get app
        Returns:
            App
        """
        return self.app

    def set_system_role(self, system_role: SystemRole):
        """ Set system role
        Args:
            (SystemRole) system_role: System role to set
        """
        self.system_role = system_role

    def get_system_role(self) -> SystemRole:
        """ Get system role
        Returns:
            SystemRole
        """
        return self.system_role

    def to_dict(self) -> dict:
        """ Convert object to dictionary
        Returns:
            dict
        """
        return {
            "id": self.get_id(),
            "user_status": self.get_user_status().to_dict(),
            "system_role": self.get_system_role().to_dict(),
            "app": self.get_app().to_dict(),
            "uuid": self.get_uuid(),
            "username": self.get_username(),
            "first_name": self.get_first_name(),
            "last_name": self.get_last_name(),
            "email": self.get_email(),
            "phone": self.get_phone(),
            "created_date": self.get_created_date()
        }

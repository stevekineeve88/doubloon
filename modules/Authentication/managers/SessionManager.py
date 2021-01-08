from flask import session

from modules.User.objects.AppUser import AppUser
from modules.User.objects.SuperUser import SuperUser


class SessionManager:
    """ Manager for handling sessions
    """
    SUPER_SESSION = "super_session"
    ADMIN_SESSION = "admin_session"

    def __init__(self):
        """ Constructor for SessionManager
        """
        self.session: session = session

    def set_super_user_session(self, token: str, user: SuperUser):
        """ Set super user session
        Args:
            (str) token:       Token string for login
            (SuperUser) user:  User to set token to
        """
        if self.SUPER_SESSION not in self.session:
            self.session[self.SUPER_SESSION] = {}
        self.session[self.SUPER_SESSION] = {token: user.to_dict()}

    def set_admin_user_session(self, token: str, user: AppUser):
        """ Set admin user session
        Args:
            (str)     token:   Token string for login
            (AppUser) user:    User to set token to
        """
        if self.ADMIN_SESSION not in self.session:
            self.session[self.ADMIN_SESSION] = {}
        self.session[self.ADMIN_SESSION] = {token: user.to_dict()}

    def set_app_user_session(self, token: str, user: AppUser):
        """ Set app user session
        Args:
            (str) token:      Token string for login
            (AppUser) user:    User to set token to
        """
        app_uuid = user.get_app().get_uuid()
        if app_uuid not in self.session:
            self.session[app_uuid] = {}
        self.session[app_uuid] = {token: user.to_dict()}

    def get_super_user_session(self, token: str) -> dict or None:
        """ Get super user session
        Args:
            (str) token: Login token
        Returns:
            dict or None
        """
        if self.SUPER_SESSION in self.session and token in self.session[self.SUPER_SESSION]:
            return self.session[self.SUPER_SESSION][token]
        return None

    def get_admin_user_session(self, token: str) -> dict or None:
        """ Get admin user session
        Args:
            (str) token: Login token
        Returns:
            dict or None
        """
        if self.ADMIN_SESSION in self.session and token in self.session[self.ADMIN_SESSION]:
            return self.session[self.ADMIN_SESSION][token]
        return None

    def get_app_user_session(self, app_uuid: str, token: str) -> dict or None:
        """ Get app user session
        Args:
            (str) app_uuid: App UUID
            (str) token:    Login token
        Returns:
            dict or None
        """
        if app_uuid in self.session and token in self.session[app_uuid]:
            return self.session[app_uuid][token]
        return None

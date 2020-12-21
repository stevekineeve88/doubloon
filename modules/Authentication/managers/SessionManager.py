from flask import session

from modules.User.objects.AppUser import AppUser
from modules.User.objects.SuperUser import SuperUser


class SessionManager:
    SUPER_SESSION = "super_session"
    ADMIN_SESSION = "admin_session"

    def __init__(self):
        self.session: session = session

    def set_super_token(self, token: str, user: SuperUser):
        if self.SUPER_SESSION not in self.session:
            self.session[self.SUPER_SESSION] = {}
        self.session[self.SUPER_SESSION] = {token: user.to_dict()}

    def set_admin_token(self, token: str, user: AppUser):
        if self.ADMIN_SESSION not in self.session:
            self.session[self.ADMIN_SESSION] = {}
        self.session[self.ADMIN_SESSION] = {token: user.to_dict()}

    def set_app_token(self, token: str, user: AppUser):
        app_name = user.get_app().get_name()
        if app_name not in self.session:
            self.session[app_name] = {}
        self.session[app_name] = {token: user.to_dict()}

    def get_super_token(self, token: str) -> dict or None:
        if self.SUPER_SESSION in self.session and token in self.session[self.SUPER_SESSION]:
            return self.session[self.SUPER_SESSION][token]
        return None

    def get_admin_token(self, token: str) -> dict or None:
        if self.ADMIN_SESSION in self.session and token in self.session[self.ADMIN_SESSION]:
            return self.session[self.ADMIN_SESSION][token]
        return None

    def get_app_token(self, app_name: str, token: str) -> dict or None:
        if app_name in self.session and token in self.session[app_name]:
            return self.session[app_name][token]
        return None

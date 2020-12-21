import random
import string

import bcrypt

from modules.App.objects.App import App
from modules.Authentication.managers.SessionManager import SessionManager
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SuperUserManager import SuperUserManager
from modules.Util.Result import Result


class AuthenticationManager:
    def __init__(self, **kwargs):
        self.super_user_manager = kwargs.get("super_user_manager") or SuperUserManager()
        self.app_user_manager = kwargs.get("app_user_manager") or AppUserManager()
        self.session_manager = kwargs.get("session_manager") or SessionManager()

    def login_super(self, username: str, password: str) -> Result:
        result = Result()
        try:
            super_user = self.super_user_manager.get_by_username(username)
            if not bcrypt.checkpw(str.encode(password), str.encode(super_user.get_password())):
                raise Exception("Password incorrect")
            token = self.__generate_token()
            self.session_manager.set_super_token(token, super_user)
            result.set_metadata_attribute("token", token)
            result.set_data([super_user])
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result

    def login_admin(self, username: str, password: str, app: App):
        pass

    def login_app(self, username: str, password: str, app: App):
        pass

    def __generate_token(self):
        return ''.join(random.choice(string.ascii_letters) for i in range(30))

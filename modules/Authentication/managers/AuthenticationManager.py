import random
import string

import bcrypt

from modules.App.objects.App import App
from modules.Authentication.managers.SessionManager import SessionManager
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SuperUserManager import SuperUserManager
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.Util.Result import Result


class AuthenticationManager:
    def __init__(self, **kwargs):
        self.__super_user_manager: SuperUserManager = kwargs.get("super_user_manager") or SuperUserManager()
        self.__app_user_manager: AppUserManager = kwargs.get("app_user_manager") or AppUserManager()
        self.__session_manager: SessionManager = kwargs.get("session_manager") or SessionManager()
        self.__system_role_manager: SystemRoleManager = kwargs.get("system_role_manager") or SystemRoleManager()

    def login_super(self, username: str, password: str) -> Result:
        result = Result()
        try:
            super_user = self.__super_user_manager.get_by_username(username)
            if not bcrypt.checkpw(str.encode(password), str.encode(super_user.get_password())):
                raise Exception("Password incorrect")
            token = self.__generate_token()
            self.__session_manager.set_super_token(token, super_user)
            result.set_metadata_attribute("token", token)
            result.set_data([super_user])
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result

    def login_admin(self, username: str, password: str, app: App):
        result = Result()
        try:
            admin_user = self.__app_user_manager.get_by_username(username, app.get_id())
            system_roles = self.__system_role_manager.get_all()
            if int(admin_user.get_system_role().get_id()) != int(system_roles.ADMIN["id"]):
                raise Exception("User has wrong role")
            if not bcrypt.checkpw(str.encode(password), str.encode(admin_user.get_password())):
                raise Exception("Password incorrect")
            token = self.__generate_token()
            self.__session_manager.set_admin_token(token, admin_user)
            result.set_metadata_attribute("token", token)
            result.set_data([admin_user])
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result

    def login_app(self, username: str, password: str, app: App):
        pass

    def __generate_token(self):
        return ''.join(random.choice(string.ascii_letters) for i in range(30))

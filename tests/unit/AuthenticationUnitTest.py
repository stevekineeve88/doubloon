import unittest
from unittest.mock import patch, MagicMock

from modules.Authentication.managers import SessionManager
from modules.Authentication.managers.AuthenticationManager import AuthenticationManager
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SuperUserManager import SuperUserManager
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.managers.UserStatusManager import UserStatusManager
from tests.unit.generators.ObjectGenerator import ObjectGenerator


class AuthenticationUnitTest(unittest.TestCase):

    SYSTEM_ROLES = ObjectGenerator.create_system_role_data_list()
    USER_STATUSES = ObjectGenerator.create_user_status_data_list()

    @classmethod
    @patch("modules.User.managers.SuperUserManager.SuperUserManager")
    @patch("modules.User.managers.AppUserManager.AppUserManager")
    @patch("modules.Authentication.managers.SessionManager.SessionManager")
    @patch("modules.User.managers.SystemRoleManager.SystemRoleManager")
    @patch("modules.User.managers.UserStatusManager.UserStatusManager")
    def setUpClass(cls,
                   super_user_manager,
                   app_user_manager,
                   session_manager,
                   system_role_manager,
                   user_status_manager
                   ) -> None:
        cls.super_user_manager: SuperUserManager = super_user_manager
        cls.app_user_manager: AppUserManager = app_user_manager
        cls.session_manager: SessionManager = session_manager
        cls.system_role_manager: SystemRoleManager = system_role_manager
        cls.system_role_manager.get_all = MagicMock(return_value=cls.SYSTEM_ROLES)
        cls.user_status_manager: UserStatusManager = user_status_manager
        cls.user_status_manager.get_all = MagicMock(return_value=cls.USER_STATUSES)
        cls.authentication_manager = AuthenticationManager(
            super_user_manager=cls.super_user_manager,
            app_user_manager=cls.app_user_manager,
            session_manager=cls.session_manager,
            system_role_manager=cls.system_role_manager,
            user_status_manager=cls.user_status_manager
        )
        cls.app = ObjectGenerator.create_app(1)

    def test_super_user_login_returns_token(self):
        username = "username"
        password = "password"
        super_user = ObjectGenerator.create_super_user(
            username=username,
            password=password
        )
        super_user.set_user_status(ObjectGenerator.create_user_status(self.USER_STATUSES.ACTIVE))
        self.super_user_manager.get_by_username = MagicMock(return_value=super_user)
        result = self.authentication_manager.login_super(username, password)
        self.assertTrue(result.get_status())
        self.assertIsNotNone(result.get_metadata_attribute("token"))

    def test_admin_user_login_returns_token(self):
        username = "username"
        password = "password"
        admin_user = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN),
            username=username,
            password=password
        )
        admin_user.set_user_status(ObjectGenerator.create_user_status(self.USER_STATUSES.ACTIVE))
        admin_user.set_app(self.app)
        self.app_user_manager.get_by_username = MagicMock(return_value=admin_user)
        result = self.authentication_manager.login_admin(username, password, self.app)
        self.app_user_manager.get_by_username.assert_called_once_with(username, self.app)
        self.assertTrue(result.get_status())
        self.assertIsNotNone(result.get_metadata_attribute("token"))

    def test_app_user_login_returns_token(self):
        username = "username"
        password = "password"
        user = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.USER),
            username=username,
            password=password
        )
        user.set_user_status(ObjectGenerator.create_user_status(self.USER_STATUSES.ACTIVE))
        user.set_app(self.app)
        self.app_user_manager.get_by_username = MagicMock(return_value=user)
        result = self.authentication_manager.login_app(username, password, self.app)
        self.app_user_manager.get_by_username.assert_called_once_with(username, self.app)
        self.assertTrue(result.get_status())
        self.assertIsNotNone(result.get_metadata_attribute("token"))

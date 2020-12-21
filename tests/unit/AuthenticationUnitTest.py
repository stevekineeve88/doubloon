import unittest
from unittest.mock import patch, MagicMock

from flask import session

from modules.Authentication.managers import SessionManager
from modules.Authentication.managers.AuthenticationManager import AuthenticationManager
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SuperUserManager import SuperUserManager
from tests.unit.generators.ObjectGenerator import ObjectGenerator


class AuthenticationUnitTest(unittest.TestCase):

    @classmethod
    @patch("modules.User.managers.SuperUserManager.SuperUserManager")
    @patch("modules.User.managers.AppUserManager.AppUserManager")
    @patch("modules.Authentication.managers.SessionManager.SessionManager")
    def setUpClass(cls, super_user_manager, app_user_manager, session_manager) -> None:
        cls.super_user_manager: SuperUserManager = super_user_manager
        cls.app_user_manager: AppUserManager = app_user_manager
        cls.session_manager: SessionManager = session_manager
        cls.authentication_manager = AuthenticationManager(
            super_user_manager=cls.super_user_manager,
            app_user_manager=cls.app_user_manager,
            session_manager=cls.session_manager
        )
        cls.app = ObjectGenerator.create_app(1)

    def test_super_user_login_returns_token(self):
        username = "username"
        password = "password"
        super_user = ObjectGenerator.create_super_user(
            username=username,
            password=password
        )
        self.super_user_manager.get_by_username = MagicMock(return_value=super_user)
        result = self.authentication_manager.login_super(username, password)
        print(result.get_message())
        self.assertTrue(result.get_status())
        self.assertIsNotNone(result.get_metadata_attribute("token"))

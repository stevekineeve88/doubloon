import unittest
from datetime import datetime
from math import ceil
from unittest.mock import patch, MagicMock

import bcrypt

from modules.App.managers.AppManager import AppManager
from modules.App.objects.App import App
from modules.User.managers.AppUserManager import AppUserManager
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.managers.UserStatusManager import UserStatusManager
from modules.User.repositories.AppUserRepo import AppUserRepo
from tests.unit.generators.MockGenerator import MockGenerator
from tests.unit.generators.ObjectGenerator import ObjectGenerator


class AppUserUnitTest(unittest.TestCase):

    USER_STATUSES = ObjectGenerator.create_user_status_data_list()
    SYSTEM_ROLES = ObjectGenerator.create_system_role_data_list()

    @classmethod
    @patch("modules.User.repositories.AppUserRepo.AppUserRepo")
    @patch("modules.User.managers.UserStatusManager.UserStatusManager")
    @patch("modules.User.managers.SystemRoleManager.SystemRoleManager")
    @patch("modules.App.managers.AppManager.AppManager")
    def setUpClass(cls, app_user_repo, user_status_manager, system_role_manager, app_manager) -> None:
        cls.app_user_repo: AppUserRepo = app_user_repo
        cls.user_status_manager: UserStatusManager = user_status_manager
        cls.user_status_manager.get_all = MagicMock(return_value=cls.USER_STATUSES)
        cls.system_role_manager: SystemRoleManager = system_role_manager
        cls.system_role_manager.get_all = MagicMock(return_value=cls.SYSTEM_ROLES)
        cls.app_id = 1
        cls.app_uuid = "abc123"
        cls.app_name = "app_name"
        cls.app_api_key = "apiKey"
        cls.app = ObjectGenerator.create_app(
            cls.app_id,
            uuid=cls.app_uuid,
            name=cls.app_name,
            api_key=cls.app_api_key
        )
        cls.app_id2 = 2
        cls.app_uuid2 = "def456"
        cls.app_name2 = "app_name_2"
        cls.app_api_key2 = "apiKeyTwo"
        cls.app2 = ObjectGenerator.create_app(
            cls.app_id2,
            uuid=cls.app_uuid2,
            name=cls.app_name2,
            api_key=cls.app_api_key2
        )
        cls.app_manager: AppManager = app_manager
        cls.app_manager.get = MagicMock(return_value=cls.app)
        cls.app_user_manager: AppUserManager = AppUserManager(
            app_user_repo=cls.app_user_repo,
            user_status_manager=cls.user_status_manager,
            system_role_manager=cls.system_role_manager,
            app_manager=cls.app_manager
        )

    def test_create_app_user_returns_app_user(self):
        user_id = 1
        uuid = "abc123"
        admin_role = self.SYSTEM_ROLES.ADMIN
        active_status = self.USER_STATUSES.ACTIVE
        username = "username"
        email = "email@email.com"
        phone = 1112223333
        first_name = "firstname"
        last_name = "lastname"
        password = "password"
        created_date = datetime.today()
        user = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(admin_role),
            username=username,
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
            created_date=created_date
        )
        self.app_user_repo.insert = MagicMock(return_value=ObjectGenerator.create_result(True, [], user_id, {}))
        user_mock = MockGenerator.create_app_user_mock(
            user,
            user_id,
            uuid,
            active_status["id"],
            admin_role["id"],
            self.app.get_id(),
            self.app.get_uuid()
        ).get_all()
        self.app_user_repo.load = MagicMock(return_value=ObjectGenerator.create_result(
            True,
            [user_mock],
            None,
            {}
        ))
        user = self.app_user_manager.create(self.app, user)
        self.app_user_repo.insert.assert_called_once_with({
            "username": username,
            "app_id": self.app.get_id(),
            "app_uuid": self.app.get_uuid(),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "password": user.get_password(),
            "user_status_id": active_status["id"],
            "system_role_id": admin_role["id"]
        })
        self.app_user_repo.load.assert_called_once_with(user_id)
        self.assertEqual(user_id, user.get_id())
        self.assertEqual(username, user.get_username())
        self.assertEqual(uuid, user.get_uuid())
        self.assertEqual(first_name, user.get_first_name())
        self.assertEqual(last_name, user.get_last_name())
        self.assertEqual(active_status["id"], user.get_user_status().get_id())
        self.assertEqual(admin_role["id"], user.get_system_role().get_id())
        self.assertEqual(self.app.get_id(), user.get_app().get_id())
        self.assertEqual(self.app.get_uuid(), user.get_app().get_uuid())
        self.assertTrue(bcrypt.checkpw(str.encode(password), str.encode(user.get_password())))

    def test_get_app_user_by_username_returns_user(self):
        username = "username"
        user_obj = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN),
            username=username
        )
        self.app_user_repo.load_by_username = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_app_user_mock(
                    user_obj,
                    user_obj.get_id(),
                    user_obj.get_uuid(),
                    self.USER_STATUSES.ACTIVE["id"],
                    self.SYSTEM_ROLES.ADMIN["id"],
                    self.app.get_id(),
                    self.app.get_uuid()
                ).get_all()
            ], None, {})
        )
        user_obj_fetch = self.app_user_manager.get_by_username(username, self.app)
        self.app_user_repo.load_by_username.assert_called_once_with(username, self.app.get_id())
        self.assertEqual(username, user_obj_fetch.get_username())

    def test_delete_app_user_returns_success(self):
        user_obj = ObjectGenerator.create_app_user(ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN))
        user_id = 1
        uuid = "abc123"
        delete_status = self.USER_STATUSES.DELETED
        self.app_user_repo.update_status = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.app_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_app_user_mock(
                    user_obj,
                    user_id,
                    uuid,
                    delete_status["id"],
                    self.SYSTEM_ROLES.ADMIN["id"],
                    self.app.get_id(),
                    self.app.get_uuid()
                ).get_all()
            ], None, {})
        )
        user = self.app_user_manager.delete(user_id)
        self.app_user_repo.update_status.assert_called_once_with(user_id, delete_status["id"])
        self.assertEqual(delete_status["id"], user.get_user_status().get_id())

    def test_disable_app_user_returns_success(self):
        user_obj = ObjectGenerator.create_app_user(ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN))
        user_id = 1
        uuid = "abc123"
        disable_status = self.USER_STATUSES.DISABLED
        self.app_user_repo.update_status = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.app_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_app_user_mock(
                    user_obj,
                    user_id,
                    uuid,
                    disable_status["id"],
                    self.SYSTEM_ROLES.ADMIN["id"],
                    self.app.get_id(),
                    self.app.get_uuid()
                ).get_all()
            ], None, {})
        )
        user = self.app_user_manager.disable(user_id)
        self.app_user_repo.update_status.assert_called_once_with(user_id, disable_status["id"])
        self.assertEqual(disable_status["id"], user.get_user_status().get_id())

    def test_activate_app_user_returns_success(self):
        user_obj = ObjectGenerator.create_app_user(ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN))
        user_id = 1
        uuid = "abc123"
        activate_status = self.USER_STATUSES.ACTIVE
        self.app_user_repo.update_status = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.app_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_app_user_mock(
                    user_obj,
                    user_id,
                    uuid,
                    activate_status["id"],
                    self.SYSTEM_ROLES.ADMIN["id"],
                    self.app.get_id(),
                    self.app.get_uuid()
                ).get_all()
            ], None, {})
        )
        user = self.app_user_manager.activate(user_id)
        self.app_user_repo.update_status.assert_called_once_with(user_id, activate_status["id"])
        self.assertEqual(activate_status["id"], user.get_user_status().get_id())

    def test_update_app_user_returns_updated_user(self):
        user_id = 1
        uuid = "abc123"
        status_id = self.USER_STATUSES.ACTIVE["id"]
        user_obj = ObjectGenerator.create_app_user(ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN))
        first_name = "New First Name"
        last_name = "New Last Name"
        email = "newemail@email.com"
        phone = 1112223344
        user_obj.set_id(user_id)
        user_obj.set_first_name(first_name)
        user_obj.set_last_name(last_name)
        user_obj.set_email(email)
        user_obj.set_phone(phone)
        user_mock = MockGenerator.create_app_user_mock(
            user_obj,
            user_id,
            uuid,
            status_id,
            self.SYSTEM_ROLES.USER["id"],
            self.app.get_id(),
            self.app.get_uuid()
        )
        self.app_user_repo.update = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.app_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [user_mock.get_all()], None, {})
        )
        updated_user = self.app_user_manager.update(user_obj)
        self.app_user_repo.update.assert_called_once_with(
            user_obj.get_id(),
            {
                "first_name": user_obj.get_first_name(),
                "last_name": user_obj.get_last_name(),
                "email": user_obj.get_email(),
                "phone": user_obj.get_phone()
            }
        )
        self.assertEqual(user_obj.get_first_name(), updated_user.get_first_name())
        self.assertEqual(user_obj.get_last_name(), updated_user.get_last_name())
        self.assertEqual(user_obj.get_email(), updated_user.get_email())
        self.assertEqual(user_obj.get_phone(), updated_user.get_phone())

    def test_update_password_returns_updated_password(self):
        old_password = "password"
        user_obj = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN),
            password=old_password
        )
        user_id = 1
        uuid = "abc123"
        status_id = self.USER_STATUSES.ACTIVE["id"]
        user_mock = MockGenerator.create_app_user_mock(
            user_obj,
            user_id,
            uuid,
            status_id,
            self.SYSTEM_ROLES.USER["id"],
            self.app.get_id(),
            self.app.get_uuid()
        )
        new_password = "NewPassword"
        self.app_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [user_mock.get_all()], None, {})
        )
        self.app_user_repo.update_password = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        updated_user = self.app_user_manager.update_password(user_id, old_password, new_password)
        self.app_user_repo.update_password.assert_called_once()
        self.assertTrue(bcrypt.checkpw(str.encode(new_password), str.encode(updated_user.get_password())))

    def test_update_password_wrong_old_password_throws_exception(self):
        user_obj = ObjectGenerator.create_app_user(ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN))
        user_id = 1
        uuid = "abc123"
        status_id = self.USER_STATUSES.ACTIVE["id"]
        user_mock = MockGenerator.create_app_user_mock(
            user_obj,
            user_id,
            uuid,
            status_id,
            self.SYSTEM_ROLES.USER["id"],
            self.app.get_id(),
            self.app.get_uuid()
        )
        new_password = "NewPassword"
        self.app_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [user_mock.get_all()], None, {})
        )
        self.app_user_repo.update_password = MagicMock()
        with self.assertRaises(Exception) as context:
            self.app_user_manager.update_password(user_id, "wrong_password", new_password)
        self.app_user_repo.update_password.assert_not_called()

    def test_search_all_app_users_returns_result(self):
        active_status = self.USER_STATUSES.ACTIVE["id"]
        search_username = "username"
        user_obj1 = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN),
            username=search_username+"1"
        )
        user_id1 = 1
        uuid1 = "abc123"
        user_obj2 = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN),
            username=search_username+"2"
        )
        user_id2 = 2
        uuid2 = "def456"
        user_mock1 = MockGenerator.create_app_user_mock(
            user_obj1,
            user_id1,
            uuid1,
            active_status,
            self.SYSTEM_ROLES.USER["id"],
            self.app.get_id(),
            self.app.get_uuid()
        )
        user_mock2 = MockGenerator.create_app_user_mock(
            user_obj2,
            user_id2,
            uuid2,
            active_status,
            self.SYSTEM_ROLES.USER["id"],
            self.app2.get_id(),
            self.app2.get_uuid()
        )
        limit = 2
        page = 1
        status = self.USER_STATUSES.ACTIVE["id"]
        order = {
            "username": -1
        }
        user_mock_updated1 = user_mock1.get_all()
        user_mock_updated2 = user_mock2.get_all()
        user_mock_updated1.update({
            "app_id": self.app.get_id(),
            "app_uuid": self.app.get_uuid(),
            "app_name": self.app.get_name(),
            "app_api_key": self.app.get_api_key(),
            "app_created_date": self.app.get_created_date()
        })
        user_mock_updated2.update({
            "app_id": self.app2.get_id(),
            "app_uuid": self.app2.get_uuid(),
            "app_name": self.app2.get_name(),
            "app_api_key": self.app2.get_api_key(),
            "app_created_date": self.app2.get_created_date()
        })
        app_results = [self.app2, self.app]
        result_set = [user_mock_updated2, user_mock_updated1]
        total_count = len(result_set)
        last_page = int(ceil(total_count / limit))
        result = ObjectGenerator.create_result(True, result_set, None, {
            "total_count": total_count,
        })
        self.app_user_repo.search_all = MagicMock(return_value=result)
        result_manager = self.app_user_manager.search_all(
            search=search_username,
            limit=limit,
            page=page,
            status=status,
            order=order
        )
        offset = (page * limit) - limit
        self.app_user_repo.search_all.assert_called_once_with(search_username, limit, offset, status, order)
        self.assertEqual(total_count, result_manager.get_metadata_attribute("total_count"))
        self.assertEqual(last_page, result_manager.get_metadata_attribute("last_page"))
        user_objs = result_manager.get_data()
        for i in range(0, len(result_set)):
            self.assertEqual(result_set[i]["username"], user_objs[i].get_username())
            user_app: App = user_objs[i].get_app()
            result_app: App = app_results[i]
            self.assertEqual(result_app.get_id(), user_app.get_id())
            self.assertEqual(result_app.get_uuid(), user_app.get_uuid())
            self.assertEqual(result_app.get_name(), user_app.get_name())
            self.assertEqual(result_app.get_api_key(), user_app.get_api_key())
            self.assertEqual(
                result_app.get_created_date().strftime("%Y-%m-%d"),
                user_app.get_created_date().strftime("%Y-%m-%d")
            )

    def search_specific_app_users_returns_result(self):
        active_status = self.USER_STATUSES.ACTIVE["id"]
        search_username = "username"
        user_obj1 = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN),
            username=search_username + "1"
        )
        user_id1 = 1
        uuid1 = "abc123"
        user_obj2 = ObjectGenerator.create_app_user(
            ObjectGenerator.create_system_role(self.SYSTEM_ROLES.ADMIN),
            username=search_username + "2"
        )
        user_id2 = 2
        uuid2 = "def456"
        user_mock1 = MockGenerator.create_app_user_mock(
            user_obj1,
            user_id1,
            uuid1,
            active_status,
            self.SYSTEM_ROLES.USER["id"],
            self.app.get_id(),
            self.app.get_uuid()
        )
        user_mock2 = MockGenerator.create_app_user_mock(
            user_obj2,
            user_id2,
            uuid2,
            active_status,
            self.SYSTEM_ROLES.USER["id"],
            self.app.get_id(),
            self.app.get_uuid()
        )
        limit = 2
        page = 1
        status = self.USER_STATUSES.ACTIVE["id"]
        order = {
            "username": -1
        }
        result_set = [user_mock2.get_all(), user_mock1.get_all()]
        total_count = len(result_set)
        last_page = int(ceil(total_count / limit))
        result = ObjectGenerator.create_result(True, result_set, None, {
            "total_count": total_count,
        })
        self.app_user_repo.search_app_users = MagicMock(return_value=result)
        result_manager = self.app_user_manager.search_app_users(
            self.app,
            search=search_username,
            limit=limit,
            page=page,
            status=status,
            order=order
        )
        offset = (page * limit) - limit
        self.app_user_repo.search_app_users.assert_called_once_with(self.app.get_name(), search_username, limit, offset, status, order)
        self.assertEqual(total_count, result_manager.get_metadata_attribute("total_count"))
        self.assertEqual(last_page, result_manager.get_metadata_attribute("last_page"))
        user_objs = result_manager.get_data()
        for i in range(0, len(result_set)):
            self.assertEqual(result_set[i]["username"], user_objs[i].get_username())
            self.assertEqual(self.app.get_id(), user_objs[i].get_app().get_id())

import unittest
from datetime import datetime
from math import ceil
from unittest.mock import patch, MagicMock

import bcrypt

from modules.User.managers.UserStatusManager import UserStatusManager
from modules.User.managers.SuperUserManager import SuperUserManager
from modules.User.repositories.SuperUserRepo import SuperUserRepo
from tests.unit.generators.MockGenerator import MockGenerator
from tests.unit.generators.ObjectGenerator import ObjectGenerator


class SuperUserUnitTest(unittest.TestCase):

    USER_STATUSES = ObjectGenerator.create_user_status_data_list()

    @classmethod
    @patch("modules.User.repositories.SuperUserRepo.SuperUserRepo")
    @patch("modules.User.managers.UserStatusManager.UserStatusManager")
    def setUpClass(cls, super_user_repo, user_status_manager) -> None:
        cls.super_user_repo: SuperUserRepo = super_user_repo
        cls.user_status_manager: UserStatusManager = user_status_manager
        cls.user_status_manager.get_all = MagicMock(return_value=cls.USER_STATUSES)
        cls.super_user_manager: SuperUserManager = SuperUserManager(
            super_user_repo=cls.super_user_repo,
            user_status_manager=cls.user_status_manager
        )

    def test_create_super_user_returns_success(self):
        user_id = 1
        uuid = "abc123"
        username = "username"
        first_name = "first_name"
        last_name = "last_name"
        email = "email@email.com"
        phone = 1112223333
        password = "password"
        created_date = datetime.today()
        user_obj = ObjectGenerator.create_super_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            created_date=created_date
        )
        self.super_user_repo.insert = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], user_id, {})
        )
        active_status = self.USER_STATUSES.ACTIVE
        self.super_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_super_user_mock(
                    user_obj,
                    user_id,
                    uuid,
                    active_status["id"]
                ).get_all()
            ], None, {}))
        user = self.super_user_manager.create(user_obj)
        self.super_user_repo.insert.assert_called_once_with({
            "username": user_obj.get_username(),
            "first_name": user_obj.get_first_name(),
            "last_name": user_obj.get_last_name(),
            "email": user_obj.get_email(),
            "phone": user_obj.get_phone(),
            "password": user_obj.get_password(),
            "user_status_id": active_status["id"]
        })
        self.assertEqual(user_id, user.get_id())
        self.assertEqual(uuid, user.get_uuid())
        self.assertEqual(active_status["id"], user.get_user_status().get_id())
        self.assertEqual(username, user.get_username())
        self.assertEqual(first_name, user.get_first_name())
        self.assertEqual(last_name, user.get_last_name())
        self.assertEqual(email, user.get_email())
        self.assertEqual(phone, user.get_phone())
        self.assertTrue(bcrypt.checkpw(str.encode(password), str.encode(user.get_password())))

    def test_get_super_user_by_username_returns_user(self):
        username = "username"
        user_obj = ObjectGenerator.create_super_user(
            username=username
        )
        self.super_user_repo.load_by_username = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_super_user_mock(
                    user_obj,
                    user_obj.get_id(),
                    user_obj.get_uuid(),
                    self.USER_STATUSES.ACTIVE["id"]
                ).get_all()
            ], None, {})
        )
        user_obj_fetch = self.super_user_manager.get_by_username(username)
        self.super_user_repo.load_by_username.assert_called_once_with(username)
        self.assertEqual(username, user_obj_fetch.get_username())

    def test_delete_super_user_returns_success(self):
        user_obj = ObjectGenerator.create_super_user()
        user_id = 1
        uuid = "abc123"
        delete_status = self.USER_STATUSES.DELETED
        self.super_user_repo.update_status = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.super_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_super_user_mock(
                    user_obj,
                    user_id,
                    uuid,
                    delete_status["id"]
                ).get_all()
            ], None, {})
        )
        user = self.super_user_manager.delete(user_id)
        self.super_user_repo.update_status.assert_called_once_with(user_id, delete_status["id"])
        self.assertEqual(delete_status["id"], user.get_user_status().get_id())

    def test_disable_super_user_returns_success(self):
        user_obj = ObjectGenerator.create_super_user()
        user_id = 1
        uuid = "abc123"
        disable_status = self.USER_STATUSES.DISABLED
        self.super_user_repo.update_status = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.super_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_super_user_mock(
                    user_obj,
                    user_id,
                    uuid,
                    disable_status["id"]
                ).get_all()
            ], None, {})
        )
        user = self.super_user_manager.disable(user_id)
        self.super_user_repo.update_status.assert_called_once_with(user_id, disable_status["id"])
        self.assertEqual(disable_status["id"], user.get_user_status().get_id())

    def test_activate_super_user_returns_success(self):
        user_obj = ObjectGenerator.create_super_user()
        user_id = 1
        uuid = "abc123"
        active_status = self.USER_STATUSES.ACTIVE
        self.super_user_repo.update_status = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.super_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [
                MockGenerator.create_super_user_mock(
                    user_obj,
                    user_id,
                    uuid,
                    active_status["id"]
                ).get_all()
            ], None, {})
        )
        user = self.super_user_manager.activate(user_id)
        self.super_user_repo.update_status.assert_called_once_with(user_id, active_status["id"])
        self.assertEqual(active_status["id"], user.get_user_status().get_id())

    def test_update_super_user_returns_updated_user(self):
        user_id = 1
        uuid = "abc123"
        status_id = self.USER_STATUSES.ACTIVE["id"]
        user_obj = ObjectGenerator.create_super_user()
        first_name = "New First Name"
        last_name = "New Last Name"
        email = "newemail@email.com"
        phone = 1112223344
        user_obj.set_id(user_id)
        user_obj.set_first_name(first_name)
        user_obj.set_last_name(last_name)
        user_obj.set_email(email)
        user_obj.set_phone(phone)
        user_mock = MockGenerator.create_super_user_mock(
            user_obj,
            user_id,
            uuid,
            status_id
        )
        self.super_user_repo.update = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        self.super_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [user_mock.get_all()], None, {})
        )
        updated_user = self.super_user_manager.update(user_obj)
        self.super_user_repo.update.assert_called_once_with(
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
        user_obj = ObjectGenerator.create_super_user(
            password=old_password
        )
        user_id = 1
        uuid = "abc123"
        status_id = self.USER_STATUSES.ACTIVE["id"]
        user_mock = MockGenerator.create_super_user_mock(
            user_obj,
            user_id,
            uuid,
            status_id
        )
        new_password = "NewPassword"
        self.super_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [user_mock.get_all()], None, {})
        )
        self.super_user_repo.update_password = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        updated_user = self.super_user_manager.update_password(user_id, old_password, new_password)
        self.super_user_repo.update_password.assert_called_once()
        self.assertTrue(bcrypt.checkpw(str.encode(new_password), str.encode(updated_user.get_password())))

    def test_update_password_wrong_old_password_throws_exception(self):
        user_obj = ObjectGenerator.create_super_user()
        user_id = 1
        uuid = "abc123"
        status_id = self.USER_STATUSES.ACTIVE["id"]
        user_mock = MockGenerator.create_super_user_mock(
            user_obj,
            user_id,
            uuid,
            status_id
        )
        new_password = "NewPassword"
        self.super_user_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [user_mock.get_all()], None, {})
        )
        self.super_user_repo.update_password = MagicMock()
        with self.assertRaises(Exception) as context:
            self.super_user_manager.update_password(user_id, "wrong_password", new_password)
        self.super_user_repo.update_password.assert_not_called()

    def test_search_super_users_returns_success(self):
        active_status = self.USER_STATUSES.ACTIVE["id"]
        search_username = "username"
        user_obj1 = ObjectGenerator.create_super_user(username=search_username+"1")
        user_id1 = 1
        uuid1 = "abc123"
        user_obj2 = ObjectGenerator.create_super_user(username=search_username+"2")
        user_id2 = 2
        uuid2 = "def456"
        user_mock1 = MockGenerator.create_super_user_mock(
            user_obj1,
            user_id1,
            uuid1,
            active_status
        )
        user_mock2 = MockGenerator.create_super_user_mock(
            user_obj2,
            user_id2,
            uuid2,
            active_status
        )
        limit = 2
        page = 1
        user_status_id = self.USER_STATUSES.ACTIVE["id"]
        order = {
            "username": -1
        }
        result_set = [user_mock2.get_all(), user_mock1.get_all()]
        total_count = len(result_set)
        last_page = int(ceil(total_count / limit))
        result = ObjectGenerator.create_result(True, result_set, None, {
            "total_count": total_count
        })
        self.super_user_repo.search = MagicMock(return_value=result)
        result_manager = self.super_user_manager.search(
            search=search_username,
            limit=limit,
            page=page,
            user_status_id=user_status_id,
            order=order
        )
        offset = (page * limit) - limit
        self.super_user_repo.search.assert_called_once_with(search_username, limit, offset, user_status_id, order)
        self.assertEqual(total_count, result_manager.get_metadata_attribute("total_count"))
        self.assertEqual(last_page, result_manager.get_metadata_attribute("last_page"))
        user_objs = result_manager.get_data()
        for i in range(0, len(result_set)):
            self.assertEqual(result_set[i]["username"], user_objs[i].get_username())

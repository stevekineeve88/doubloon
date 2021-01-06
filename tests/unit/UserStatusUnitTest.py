import unittest
from unittest.mock import patch, MagicMock

from modules.User.managers.UserStatusManager import UserStatusManager
from modules.User.repositories.UserStatusRepo import UserStatusRepo
from tests.unit.generators.ObjectGenerator import ObjectGenerator


class SystemRoleUnitTest(unittest.TestCase):

    @classmethod
    @patch("modules.User.repositories.UserStatusRepo.UserStatusRepo")
    def setUpClass(cls, user_status_repo) -> None:
        cls.user_status_repo: UserStatusRepo = user_status_repo
        cls.user_status_manager: UserStatusManager = UserStatusManager(
            user_status_repo=cls.user_status_repo
        )

    def test_get_all_user_statuses_returns_datalist(self):
        statuses = [
            {
                "id": 1,
                "const": "ACTIVE",
                "description": "active"
            }
        ]
        self.user_status_repo.load_all = MagicMock(return_value=ObjectGenerator.create_result(
            True,
            statuses,
            None,
            {}
        ))
        statuses_datalist = self.user_status_manager.get_all()
        self.user_status_repo.load_all.assert_called_once()
        fetched_item = statuses_datalist.get(statuses[0]["id"])
        self.assertIsNotNone(fetched_item)
        self.assertEqual(statuses[0]["const"], fetched_item["const"])
        self.assertEqual(statuses[0]["description"], fetched_item["description"])

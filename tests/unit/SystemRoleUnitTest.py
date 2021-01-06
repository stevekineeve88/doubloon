import unittest
from unittest.mock import patch, MagicMock

from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.repositories.SystemRoleRepo import SystemRoleRepo
from tests.unit.generators.ObjectGenerator import ObjectGenerator


class SystemRoleUnitTest(unittest.TestCase):

    @classmethod
    @patch("modules.User.repositories.SystemRoleRepo.SystemRoleRepo")
    def setUpClass(cls, system_role_repo) -> None:
        cls.system_role_repo: SystemRoleRepo = system_role_repo
        cls.system_role_manager: SystemRoleManager = SystemRoleManager(
            system_role_repo=cls.system_role_repo
        )

    def test_get_all_system_roles_returns_datalist(self):
        roles = [
            {
                "id": 1,
                "const": "ADMIN",
                "description": "admin"
            }
        ]
        self.system_role_repo.load_all = MagicMock(return_value=ObjectGenerator.create_result(
            True,
            roles,
            None,
            {}
        ))
        roles_datalist = self.system_role_manager.get_all()
        self.system_role_repo.load_all.assert_called_once()
        fetched_item = roles_datalist.get(roles[0]["id"])
        self.assertIsNotNone(fetched_item)
        self.assertEqual(roles[0]["const"], fetched_item["const"])
        self.assertEqual(roles[0]["description"], fetched_item["description"])

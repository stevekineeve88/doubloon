import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import bcrypt

from modules.App.managers.AppManager import AppManager
from modules.App.repositories.AppRepo import AppRepo
from tests.unit.generators.MockGenerator import MockGenerator
from tests.unit.generators.ObjectGenerator import ObjectGenerator


class AppUnitTest(unittest.TestCase):
    @patch("modules.App.repositories.AppRepo.AppRepo")
    def setUp(self, app_repo) -> None:
        self.app_repo: AppRepo = app_repo
        self.app_manager: AppManager = AppManager(
            app_repo=self.app_repo
        )

    def test_create_app_returns_app(self):
        name = "app_name"
        app_id = 1
        api_key = "apiKey"
        uuid = "abc123"
        self.app_repo.create = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], app_id, {})
        )
        self.app_manager.get = MagicMock(
            return_value=ObjectGenerator.create_app(
                app_id,
                api_key=api_key,
                name=name,
                uuid=uuid
            )
        )
        self.app_repo.create_partition = MagicMock(
            return_value=ObjectGenerator.create_result(True, [], None, {})
        )
        app = self.app_manager.create(name)
        self.app_repo.create.assert_called_once()
        self.app_repo.create_partition.assert_called_once()
        self.assertEqual(app_id, app.get_id())
        self.assertEqual(name, app.get_name())
        self.assertEqual(uuid, app.get_uuid())
        self.assertEqual(api_key, app.get_api_key())
    
    def test_create_app_invalid_name_throws_exception(self):
        name = "Invalid_Name_123"
        self.app_repo.create = MagicMock(return_value=None)
        with self.assertRaises(Exception) as context:
            self.app_manager.create(name)
        self.app_repo.create.assert_not_called()

    def test_get_app_returns_app(self):
        app_id = 1
        api_key = "apiKey"
        name = "name"
        uuid = "abc123"
        created_date = datetime.today()
        app = ObjectGenerator.create_app(
            app_id,
            api_key=api_key,
            name=name,
            uuid=uuid,
            created_date=created_date
        )
        app_mock = MockGenerator.create_app_mock(app)
        self.app_repo.load = MagicMock(
            return_value=ObjectGenerator.create_result(True, [app_mock.get_all()], None, {})
        )
        fetch_app_obj = self.app_manager.get(app_id)
        self.app_repo.load.assert_called_once_with(app_id)
        self.assertEqual(app.get_id(), fetch_app_obj.get_id())
        self.assertEqual(app.get_api_key(), fetch_app_obj.get_api_key())
        self.assertEqual(app.get_uuid(), fetch_app_obj.get_uuid())
        self.assertEqual(app.get_name(), fetch_app_obj.get_name())
        self.assertEqual(app.get_created_date(), fetch_app_obj.get_created_date())

    def test_search_apps_returns_result(self):
        search_name = "name"
        app1 = ObjectGenerator.create_app(1, name=f'{search_name}1')
        app_mock1 = MockGenerator.create_app_mock(app1)
        app2 = ObjectGenerator.create_app(2, name=f'{search_name}2')
        app_mock2 = MockGenerator.create_app_mock(app2)
        limit = 2
        page = 1
        order = {
            "name": -1
        }
        result_set = [app_mock2.get_all(), app_mock1.get_all()]
        total_count = len(result_set)
        result_start = 0
        result_end = len(result_set) - 1
        next_offset = len(result_set)
        result = ObjectGenerator.create_result(True, result_set, None, {
            "total_count": total_count,
            "result_start": result_start,
            "result_end": result_end,
            "next_offset": next_offset
        })
        self.app_repo.search = MagicMock(return_value=result)
        result_manager = self.app_manager.search(
            search=search_name,
            limit=limit,
            page=page,
            order=order
        )
        offset = (page * limit) - limit
        self.app_repo.search.assert_called_once_with(search_name, limit, offset, order)
        self.assertEqual(total_count, result_manager.get_metadata_attribute("total_count"))
        self.assertEqual(result_start, result_manager.get_metadata_attribute("result_start"))
        self.assertEqual(result_end, result_manager.get_metadata_attribute("result_end"))
        self.assertEqual(next_offset, result_manager.get_metadata_attribute("next_offset"))
        app_objects = result_manager.get_data()
        for i in range(0, len(result_set)):
            self.assertEqual(result_set[i]["name"], app_objects[i].get_name())

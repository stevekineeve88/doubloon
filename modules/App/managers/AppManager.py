import random
import string
import re
import sys
from math import ceil

from modules.App.objects.App import App
from modules.App.repositories.AppRepo import AppRepo


class AppManager:
    def __init__(self, **kwargs):
        self.__app_repo: AppRepo = kwargs.get("app_repo") or AppRepo()

    def create(self, name: str) -> App:
        pattern = "^[a-z_]*$"
        if not re.match(pattern, name):
            raise Exception("Could not create App: Does not match naming convention")
        result = self.__app_repo.create(name, self.__generate_api_key())
        if not result.get_status():
            raise Exception("Could not create App: App may already exist")
        app = self.get(result.get_insert_id())
        if app.get_name() != name:
            self.hard_delete(app.get_id())
            raise Exception("Could not create App: App name is too long")
        result = self.__app_repo.create_partition(name, app.get_uuid())
        if not result.get_status():
            self.hard_delete(app.get_id())
            raise Exception("Could not create App: Failed to allocate partition")
        return app

    def get(self, app_id: int) -> App:
        result = self.__app_repo.load(app_id)
        if not result.get_status() or not result.get_data():
            raise Exception(result.get_message())
        return self.__build_app_obj(result.get_data()[0])

    def get_by_name(self, app_name: str) -> App:
        result = self.__app_repo.load_by_name(app_name)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find app")
        return self.__build_app_obj(result.get_data()[0])
    
    def get_by_uuid(self, app_uuid) -> App:
        result = self.__app_repo.load_by_uuid(app_uuid)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find app")
        return self.__build_app_obj(result.get_data()[0])

    def search(self, **kwargs):
        search = kwargs.get("search") or ""
        limit = kwargs.get("limit") or 100
        page = kwargs.get("page") or 1
        offset = (limit * page) - limit if page > 0 else 0
        order = kwargs.get("order") or {}
        result = self.__app_repo.search(search, limit, offset, order)
        if not result.get_status():
            raise Exception("Could not fetch apps")
        data = result.get_data()
        result.set_metadata_attribute("last_page", int(ceil(result.get_metadata_attribute("total_count") / limit)))
        apps = []
        for datum in data:
            apps.append(self.__build_app_obj(datum))
        result.set_data(apps)
        return result

    def hard_delete(self, app_id: int) -> bool:
        result = self.__app_repo.delete(app_id)
        if not result.get_status():
            return False
        return True

    def __build_app_obj(self, data: dict) -> App:
        app = App()
        app.set_id(data["id"])
        app.set_uuid(data["uuid"])
        app.set_api_key(data["api_key"])
        app.set_name(data["name"])
        app.set_created_date(data["created_date"])
        return app

    def __generate_api_key(self) -> str:
        return ''.join(random.choice(string.ascii_letters) for i in range(30))

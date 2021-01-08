import random
import string
import re
from math import ceil

from modules.App.objects.App import App
from modules.App.repositories.AppRepo import AppRepo
from modules.Util.Result import Result


class AppManager:
    """ Manager class for handling app CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for AppManager
        Args:
            **kwargs: Dependencies if needed
                (AppRepo) app_repo
        """
        self.__app_repo: AppRepo = kwargs.get("app_repo") or AppRepo()

    def create(self, name: str) -> App:
        """ Create an app
        Args:
            (str) name: Name of app
        Returns:
            App
        """
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
        """ Get app by ID
        Args:
            (int) app_id: App ID
        Returns:
            App
        """
        result = self.__app_repo.load(app_id)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find app")
        return self.__build_app_obj(result.get_data()[0])

    def get_by_name(self, app_name: str) -> App:
        """ Get app by name
        Args:
            (str) app_name: App name
        Returns:
            App
        """
        result = self.__app_repo.load_by_name(app_name)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find app")
        return self.__build_app_obj(result.get_data()[0])
    
    def get_by_uuid(self, app_uuid) -> App:
        """ Get app by UUID
        Args:
            (str) app_uuid: App UUID
        Returns:
            App
        """
        result = self.__app_repo.load_by_uuid(app_uuid)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find app")
        return self.__build_app_obj(result.get_data()[0])

    def search(self, **kwargs) -> Result:
        """ Search for apps
        Args:
            **kwargs: Arguments for search
                (str) search: Search string
                (int) limit:  Limit of result
                (int) page:   Page of result
                (dict) order: Order by a column key and ASC(1) or DESC(-1)
        Returns:
            Result
        """
        limit = kwargs.get("limit") or 100
        page = kwargs.get("page") or 1
        result = self.__app_repo.search(
            kwargs.get("search") or "",
            limit,
            (limit * page) - limit if page > 0 else 0,
            kwargs.get("order") or {}
        )
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
        """ Hard delete an app
        Args:
            (int) app_id: App ID
        Returns:
            bool
        """
        result = self.__app_repo.delete(app_id)
        if not result.get_status():
            return False
        return True

    @classmethod
    def __build_app_obj(cls, data: dict) -> App:
        """ Build App object
        Args:
            (dict) data: Data for creating object
                (int) id:                App ID
                (str) uuid:              App UUID
                (str) api_key:           API Key
                (str) name:              App Name
                (datetime) created_date: Creation date for app
        Returns:
            App
        """
        app = App()
        app.set_id(data["id"])
        app.set_uuid(data["uuid"])
        app.set_api_key(data["api_key"])
        app.set_name(data["name"])
        app.set_created_date(data["created_date"])
        return app

    @classmethod
    def __generate_api_key(cls) -> str:
        """ Generate API key
        Returns:
            str
        """
        return ''.join(random.choice(string.ascii_letters) for i in range(30))

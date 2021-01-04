from math import ceil

import bcrypt

from modules.App.managers.AppManager import AppManager
from modules.App.objects.App import App
from modules.User.managers.SystemRoleManager import SystemRoleManager
from modules.User.managers.UserStatusManager import UserStatusManager
from modules.User.objects.AppUser import AppUser
from modules.User.objects.SystemRole import SystemRole
from modules.User.objects.UserStatus import UserStatus
from modules.User.repositories.AppUserRepo import AppUserRepo
from modules.Util.DataList import DataList


class AppUserManager:
    def __init__(self, **kwargs):
        self.app_user_repo: AppUserRepo = kwargs.get("app_user_repo") or AppUserRepo()
        user_status_manager: UserStatusManager = kwargs.get("user_status_manager") or UserStatusManager()
        system_role_manager: SystemRoleManager = kwargs.get("system_role_manager") or SystemRoleManager()
        self.user_statuses: DataList = user_status_manager.get_all()
        self.system_roles: DataList = system_role_manager.get_all()
        self.app_manager: AppManager = kwargs.get("app_manager") or AppManager()

    def create(self, app: App, user: AppUser) -> AppUser:
        data = {
            "username": user.get_username(),
            "app_id": app.get_id(),
            "app_uuid": app.get_uuid(),
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "email": user.get_email(),
            "phone": user.get_phone(),
            "password": user.get_password(),
            "user_status_id": self.user_statuses.ACTIVE["id"],
            "system_role_id": user.get_system_role().get_id()
        }
        result = self.app_user_repo.insert(data)
        if not result.get_status():
            raise Exception(result.get_message())
        return self.get(result.get_insert_id())

    def get(self, app_user_id: int) -> AppUser:
        result = self.app_user_repo.load(app_user_id)
        if not result.get_status() or not result.get_data():
            raise Exception(result.get_message())
        data = result.get_data()[0]
        app_id = data["app_id"]
        app = self.app_manager.get(app_id)
        return self.__build_app_user_obj(result.get_data()[0], app)

    def get_by_username(self, username: str, app_id: id) -> AppUser:
        result = self.app_user_repo.load_by_username(username, app_id)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find user")
        app = self.app_manager.get(app_id)
        return self.__build_app_user_obj(result.get_data()[0], app)

    def delete(self, app_user_id: int) -> AppUser:
        self.app_user_repo.update_status(app_user_id, self.user_statuses.DELETED["id"])
        return self.get(app_user_id)

    def disable(self, app_user_id: int) -> AppUser:
        self.app_user_repo.update_status(app_user_id, self.user_statuses.DISABLED["id"])
        return self.get(app_user_id)

    def activate(self, app_user_id: int) -> AppUser:
        self.app_user_repo.update_status(app_user_id, self.user_statuses.ACTIVE["id"])
        return self.get(app_user_id)

    def search_app_users(self, app: App, **kwargs):
        search = kwargs.get("search") or ""
        limit = kwargs.get("limit") or 100
        page = kwargs.get("page") or 1
        offset = (limit * page) - limit if page > 0 else 0
        status = kwargs.get("status") or self.user_statuses.ACTIVE["id"]
        order = kwargs.get("order") or {}
        result = self.app_user_repo.search_app_users(
            app.get_name(),
            search,
            limit,
            offset,
            status,
            order
        )
        if not result.get_status():
            raise Exception("Could not fetch users")
        result.set_metadata_attribute("last_page", int(ceil(result.get_metadata_attribute("total_count") / limit)))
        data = result.get_data()
        users = []
        for datum in data:
            users.append(self.__build_app_user_obj(datum, app))
        result.set_data(users)
        return result

    def search_all(self, **kwargs):
        search = kwargs.get("search") or ""
        limit = kwargs.get("limit") or 100
        page = kwargs.get("page") or 1
        offset = (limit * page) - limit if page > 0 else 0
        status = kwargs.get("status") or self.user_statuses.ACTIVE["id"]
        order = kwargs.get("order") or {
            "id": 1
        }
        result = self.app_user_repo.search_all(search, limit, offset, status, order)
        if not result.get_status():
            return result
        data = result.get_data()
        users = []
        for datum in data:
            app = App()
            app.set_id(datum["app_id"])
            app.set_uuid(datum["app_uuid"])
            app.set_name(datum["app_name"])
            app.set_api_key(datum["app_api_key"])
            app.set_created_date(datum["app_created_date"])
            users.append(self.__build_app_user_obj(datum, app))
        result.set_data(users)
        return result

    def update(self, user: AppUser):
        data = {
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "email": user.get_email(),
            "phone": user.get_phone()
        }
        self.app_user_repo.update(user.get_id(), data)
        return self.get(user.get_id())

    def update_password(self, app_user_id: int, old_password: str, new_password: str) -> AppUser:
        user = self.get(app_user_id)
        if not bcrypt.checkpw(str.encode(old_password), str.encode(user.get_password())):
            raise Exception("Password authentication failed for old password")
        user.set_password(new_password)
        self.app_user_repo.update_password(app_user_id, user.get_password())
        return user

    def __build_app_user_obj(self, data: dict, app: App):
        status_data = self.user_statuses.get(data["user_status_id"])
        system_role = self.system_roles.get(data["system_role_id"])
        user = AppUser()
        user.set_id(data["id"])
        user.set_user_status(UserStatus(status_data["id"], status_data["const"], status_data["description"]))
        user.set_system_role(SystemRole(system_role["id"], system_role["const"], system_role["description"]))
        user.set_app(app)
        user.set_uuid(data["uuid"])
        user.set_username(data["username"])
        user.set_first_name(data["first_name"])
        user.set_last_name(data["last_name"])
        user.set_password_encrypted(data["password"])
        user.set_email(data["email"])
        user.set_phone(data["phone"])
        user.set_created_date(data["created_date"])
        return user

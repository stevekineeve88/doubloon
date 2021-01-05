from datetime import datetime

from modules.App.objects.App import App
from modules.User.objects.AppUser import AppUser
from modules.User.objects.SuperUser import SuperUser
from modules.User.objects.SystemRole import SystemRole
from modules.User.objects.UserStatus import UserStatus
from modules.Util.DataList import DataList
from modules.Util.Result import Result


class ObjectGenerator:
    @staticmethod
    def create_result(status, data: list, insert_id: int or None, metadata: dict):
        result = Result()
        result.set_status(status)
        result.set_data(data)
        result.set_insert_id(insert_id)
        result.set_metadata(metadata)
        return result

    @staticmethod
    def create_super_user(**kwargs):
        user = SuperUser()
        user.set_username(kwargs.get("username") or "username")
        user.set_first_name(kwargs.get("first_name") or "first_name")
        user.set_last_name(kwargs.get("last_name") or "last_name")
        user.set_email(kwargs.get("email") or "email@email.com")
        user.set_phone(kwargs.get("phone") or 1112223333)
        user.set_password(kwargs.get("password") or "password")
        user.set_created_date(kwargs.get("created_date") or datetime.today())
        return user

    @staticmethod
    def create_app_user(system_status: SystemRole, **kwargs) -> AppUser:
        user = AppUser()
        user.set_username(kwargs.get("username") or "username")
        user.set_system_role(system_status)
        user.set_first_name(kwargs.get("first_name") or "first_name")
        user.set_last_name(kwargs.get("last_name") or "last_name")
        user.set_email(kwargs.get("email") or "email@email.com")
        user.set_phone(kwargs.get("phone") or 1112223333)
        user.set_password(kwargs.get("password") or "password")
        user.set_created_date(kwargs.get("created_date") or datetime.today())
        return user

    @staticmethod
    def create_app(app_id, **kwargs):
        app = App()
        app.set_id(app_id)
        app.set_api_key(kwargs.get("api_key") or "apiKey")
        app.set_uuid(kwargs.get("uuid") or "abc123")
        app.set_name(kwargs.get("name") or "name")
        app.set_created_date(kwargs.get("created_date") or datetime.today())
        return app

    @staticmethod
    def create_user_status_data_list() -> DataList:
        return DataList([
            {
                "id": 1,
                "const": "DELETED",
                "description": "deleted"
            },
            {
                "id": 2,
                "const": "DISABLED",
                "description": "disabled"
            },
            {
                "id": 3,
                "const": "ACTIVE",
                "description": "active"
            }
        ])

    @staticmethod
    def create_system_role_data_list():
        return DataList([
            {
                "id": 1,
                "const": "ADMIN",
                "description": "admin"
            },
            {
                "id": 2,
                "const": "USER",
                "description": "user"
            }
        ])

    @staticmethod
    def create_system_role(data_list_item: dict) -> SystemRole:
        return SystemRole(data_list_item["id"], data_list_item["const"], data_list_item["description"])

    @staticmethod
    def create_user_status(data_list_item: dict) -> UserStatus:
        return UserStatus(data_list_item["id"], data_list_item["const"], data_list_item["description"])

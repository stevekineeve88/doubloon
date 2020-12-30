import bcrypt

from modules.User.managers.UserStatusManager import UserStatusManager
from modules.User.objects.UserStatus import UserStatus
from modules.User.objects.SuperUser import SuperUser
from modules.User.repositories.SuperUserRepo import SuperUserRepo
from modules.Util.Result import Result


class SuperUserManager:
    def __init__(self, **kwargs):
        self.super_user_repo: SuperUserRepo = kwargs.get('super_user_repo') or SuperUserRepo()
        user_status_manager = kwargs.get('user_status_manager') or UserStatusManager()
        self.user_statuses = user_status_manager.get_all()

    def create(self, user: SuperUser) -> SuperUser:
        data = {
            "username": user.get_username(),
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "email": user.get_email(),
            "phone": user.get_phone(),
            "password": user.get_password(),
            "user_status_id": self.user_statuses.ACTIVE["id"]
        }
        result = self.super_user_repo.insert(data)
        if not result.get_status():
            raise Exception("Could not create super user")
        return self.get(result.get_insert_id())

    def get(self, super_user_id: int) -> SuperUser:
        result = self.super_user_repo.load(super_user_id)
        if not result.get_status() or not result.get_data():
            raise Exception(result.get_message())
        return self.__build_super_user_obj(result.get_data()[0])

    def get_by_username(self, username: str) -> SuperUser:
        result = self.super_user_repo.load_by_username(username)
        if not result.get_status() or not result.get_data():
            raise Exception(result.get_message())
        return self.__build_super_user_obj(result.get_data()[0])

    def delete(self, super_user_id: int) -> SuperUser:
        self.super_user_repo.update_status(super_user_id, self.user_statuses.DELETED["id"])
        return self.get(super_user_id)

    def disable(self, super_user_id: int) -> SuperUser:
        self.super_user_repo.update_status(super_user_id, self.user_statuses.DISABLED["id"])
        return self.get(super_user_id)

    def activate(self, super_user_id: int) -> SuperUser:
        self.super_user_repo.update_status(super_user_id, self.user_statuses.ACTIVE["id"])
        return self.get(super_user_id)

    def search(self, **kwargs) -> Result:
        search = kwargs.get("search") or ""
        limit = kwargs.get("limit") or 100
        page = kwargs.get("page") or 1
        offset = (limit * page) - limit if page > 0 else 0
        user_status_id = kwargs.get("user_status_id") or self.user_statuses.ACTIVE["id"]
        order = kwargs.get("order") or {}
        result = self.super_user_repo.search(search, limit, offset, user_status_id, order)
        if not result.get_status():
            raise Exception("Could not fetch users")
        data = result.get_data()
        result.set_metadata_attribute("last_page", int(result.get_metadata_attribute("total_count") / limit))
        users = []
        for datum in data:
            users.append(self.__build_super_user_obj(datum))
        result.set_data(users)
        return result

    def update(self, user: SuperUser) -> SuperUser:
        data = {
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "email": user.get_email(),
            "phone": user.get_phone()
        }
        self.super_user_repo.update(user.get_id(), data)
        return self.get(user.get_id())

    def update_password(self, super_user_id: int, old_password: str, new_password: str):
        user = self.get(super_user_id)
        if not bcrypt.checkpw(str.encode(old_password), str.encode(user.get_password())):
            raise Exception("Password authentication failed for old password")
        user.set_password(new_password)
        self.super_user_repo.update_password(super_user_id, user.get_password())
        return user

    def __build_super_user_obj(self, data) -> SuperUser:
        status_data = self.user_statuses.get(data["user_status_id"])
        user = SuperUser()
        user.set_id(data["id"])
        user.set_user_status(UserStatus(status_data["id"], status_data["const"], status_data["description"]))
        user.set_uuid(data["uuid"])
        user.set_username(data["username"])
        user.set_first_name(data["first_name"])
        user.set_last_name(data["last_name"])
        user.set_password_encrypted(data["password"])
        user.set_email(data["email"])
        user.set_phone(data["phone"])
        user.set_created_date(data["created_date"])
        return user

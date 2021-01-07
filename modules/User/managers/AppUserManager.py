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
    """ Manager for handling app user CRUD operations
    """

    def __init__(self, **kwargs):
        """ Constructor for AppUserManager
        Args:
            **kwargs: Dependencies if needed
                (AppUserRepo) app_user_repo
                (UserStatusManager) user_status_manager
                (SystemRoleManager) system_role_manager
                (AppManager) app_manager
        """
        self.app_user_repo: AppUserRepo = kwargs.get("app_user_repo") or AppUserRepo()
        self.app_manager: AppManager = kwargs.get("app_manager") or AppManager()
        user_status_manager: UserStatusManager = kwargs.get("user_status_manager") or UserStatusManager()
        system_role_manager: SystemRoleManager = kwargs.get("system_role_manager") or SystemRoleManager()
        self.user_statuses: DataList = user_status_manager.get_all()
        self.system_roles: DataList = system_role_manager.get_all()

    def create(self, app: App, user: AppUser) -> AppUser:
        """ Create app user
        Args:
            (App) app:        App to add user to
            (AppUser) user:   AppUser object to create off of
        Returns:
            AppUser
        """
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
            raise Exception("Could not create user")
        return self.get(result.get_insert_id())

    def get(self, app_user_id: int) -> AppUser:
        """ Get app user by ID
        Args:
            app_user_id: App user ID
        Returns:
            AppUser
        """
        result = self.app_user_repo.load(app_user_id)
        if not result.get_status() or not result.get_data():
            raise Exception(result.get_message())
        data = result.get_data()[0]
        app_id = data["app_id"]
        app = self.app_manager.get(app_id)
        return self.__build_app_user_obj(data, app)

    def get_by_username(self, username: str, app: App) -> AppUser:
        """ Get app user by username
        Args:
            (str) username: App user username
            (App) app:      App to search for username
        Returns:
            AppUser
        """
        result = self.app_user_repo.load_by_username(username, app.get_id())
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find user")
        return self.__build_app_user_obj(result.get_data()[0], app)

    def delete(self, app_user_id: int) -> AppUser:
        """ Soft delete an app user by ID
        Args:
            (int) app_user_id: App user ID
        Returns:
            AppUser
        """
        result = self.app_user_repo.update_status(app_user_id, self.user_statuses.DELETED["id"])
        if not result.get_status():
            raise Exception("Could not delete user")
        return self.get(app_user_id)

    def disable(self, app_user_id: int) -> AppUser:
        """ Disable an app user by ID
        Args:
            (int) app_user_id: App user ID
        Returns:
            AppUser
        """
        result = self.app_user_repo.update_status(app_user_id, self.user_statuses.DISABLED["id"])
        if not result.get_status():
            raise Exception("Could not disable user")
        return self.get(app_user_id)

    def activate(self, app_user_id: int) -> AppUser:
        """ Activate an app user by ID
        Args:
            (int) app_user_id: App user ID
        Returns:
            AppUser
        """
        result = self.app_user_repo.update_status(app_user_id, self.user_statuses.ACTIVE["id"])
        if not result.get_status():
            raise Exception("Could not activate user")
        return self.get(app_user_id)

    def search_app_users(self, app: App, **kwargs):
        """ Search app users by app
        Args:
            (App) app:          App to search in
            (kwargs) **kwargs:  Arguments for search
                (str) search:        Search string
                (int) limit:         Limit of result
                (int) page:          Page of result
                (int) user_status_id User status ID to partition search
                (dict) order:        Order with key column and ASC(1) or DESC(-1)
        Returns:
            Result
        """
        limit = kwargs.get("limit") or 100
        page = kwargs.get("page") or 1
        result = self.app_user_repo.search_app_users(
            app.get_name(),
            kwargs.get("search") or "",
            limit,
            (limit * page) - limit if page > 0 else 0,
            kwargs.get("user_status_id") or self.user_statuses.ACTIVE["id"],
            kwargs.get("order") or {}
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

    def update(self, user: AppUser) -> AppUser:
        """ Update app user
        Args:
            (AppUser) user: AppUser to update
        Returns:
            AppUser
        """
        data = {
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "email": user.get_email(),
            "phone": user.get_phone()
        }
        app_user_id = user.get_id()
        result = self.app_user_repo.update(app_user_id, data)
        if not result.get_status():
            raise Exception("Could not update user")
        return self.get(app_user_id)

    def update_password(self, app_user_id: int, old_password: str, new_password: str) -> AppUser:
        """ Update app user password by ID
        Args:
            (int) app_user_id:   App user ID
            (str) old_password:  Old password
            (str) new_password:  New password
        Returns:
            AppUser
        """
        user = self.get(app_user_id)
        if not bcrypt.checkpw(str.encode(old_password), str.encode(user.get_password())):
            raise Exception("Password authentication failed for old password")
        user.set_password(new_password)
        result = self.app_user_repo.update_password(app_user_id, user.get_password())
        if not result.get_status():
            raise Exception("Failed to update password")
        return user

    def __build_app_user_obj(self, data: dict, app: App) -> AppUser:
        """ Build AppUser object
        Args:
            (dict) data: Data for creating object
                (int) id:                   App user ID
                (int) user_status_id:       User status ID
                (int) system_role_id:       System role ID
                (str) uuid:                 App user UUID
                (str) username:             App user username
                (str) first_name:           App user first name
                (str) last_name:            App user last_name
                (str) password:             App user password encrypted
                (str) email:                App user email
                (str) phone:                App user phone
                (datetime) created_date:    App user created date
            (App) app:   App object for referencing
        Returns:
            AppUser
        """
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

from math import ceil

import bcrypt

from modules.User.managers.UserStatusManager import UserStatusManager
from modules.User.objects.UserStatus import UserStatus
from modules.User.objects.SuperUser import SuperUser
from modules.User.repositories.SuperUserRepo import SuperUserRepo
from modules.Util.Result import Result


class SuperUserManager:
    """ Manager class for handling super user CRUD operations
    """

    def __init__(self, **kwargs):
        """ Constructor for SuperUserManager
        Args:
            **kwargs: Dependencies if needed
                (SuperUserRepo) super_user_repo
                (UserStatusManager) user_status_manager
        """
        self.super_user_repo: SuperUserRepo = kwargs.get('super_user_repo') or SuperUserRepo()
        user_status_manager = kwargs.get('user_status_manager') or UserStatusManager()
        self.user_statuses = user_status_manager.get_all()

    def create(self, user: SuperUser) -> SuperUser:
        """ Create super user
        Args:
            (SuperUser) user: Super user to create
        Returns:
            SuperUser
        """
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
        """ Get super user by ID
        Args:
            (int) super_user_id: Super user ID
        Returns:
            SuperUser
        """
        result = self.super_user_repo.load(super_user_id)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not fetch super user")
        return self.__build_super_user_obj(result.get_data()[0])

    def get_by_username(self, username: str) -> SuperUser:
        """ Get super user by username
        Args:
            (str) username: Super user username
        Returns:
            SuperUser
        """
        result = self.super_user_repo.load_by_username(username)
        if not result.get_status() or not result.get_data():
            raise Exception("Could not find user")
        return self.__build_super_user_obj(result.get_data()[0])

    def delete(self, super_user_id: int) -> SuperUser:
        """ Soft delete super user by ID
        Args:
            (int) super_user_id: Super user ID
        Returns:
            SuperUser
        """
        result = self.super_user_repo.update_status(super_user_id, self.user_statuses.DELETED["id"])
        if not result.get_status():
            raise Exception("Could not delete user")
        return self.get(super_user_id)

    def disable(self, super_user_id: int) -> SuperUser:
        """ Disable super user by ID
        Args:
            (int) super_user_id: Super user ID
        Returns:
            SuperUser
        """
        result = self.super_user_repo.update_status(super_user_id, self.user_statuses.DISABLED["id"])
        if not result.get_status():
            raise Exception("Could not disable user")
        return self.get(super_user_id)

    def activate(self, super_user_id: int) -> SuperUser:
        """ Activate super user by ID
        Args:
            (int) super_user_id: Super user ID
        Returns:
            SuperUser
        """
        result = self.super_user_repo.update_status(super_user_id, self.user_statuses.ACTIVE["id"])
        if not result.get_status():
            raise Exception("Could not activate user")
        return self.get(super_user_id)

    def search(self, **kwargs) -> Result:
        """ Search super users
        Args:
            **kwargs: Arguments for search
                (str) search:           Search string
                (int) limit:            Limit of result
                (int) page:             Page of result
                (int) user_status_id:   User status ID to partition by
                (dict) order:           Order with column key and ASC(1) or DESC(-1)
        Returns:
            Result
        """
        limit = kwargs.get("limit") or 100
        page = kwargs.get("page") or 1
        result = self.super_user_repo.search(
            kwargs.get("search") or "",
            limit,
            (limit * page) - limit if page > 0 else 0,
            kwargs.get("user_status_id") or self.user_statuses.ACTIVE["id"],
            kwargs.get("order") or {}
        )
        if not result.get_status():
            raise Exception("Could not fetch users")
        data = result.get_data()
        result.set_metadata_attribute("last_page", int(ceil(result.get_metadata_attribute("total_count") / limit)))
        users = []
        for datum in data:
            users.append(self.__build_super_user_obj(datum))
        result.set_data(users)
        return result

    def update(self, user: SuperUser) -> SuperUser:
        """ Update super user
        Args:
            (SuperUser) user: Super user to update
        Returns:
            SuperUser
        """
        data = {
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "email": user.get_email(),
            "phone": user.get_phone()
        }
        result = self.super_user_repo.update(user.get_id(), data)
        if not result.get_status():
            raise Exception("Could not update super user")
        return self.get(user.get_id())

    def update_password(self, super_user_id: int, old_password: str, new_password: str) -> SuperUser:
        """ Update super user password by ID
        Args:
            (int) super_user_id: Super user ID
            (str) old_password:  Old password
            (str) new_password:  New password
        Returns:
            SuperUser
        """
        user = self.get(super_user_id)
        if not bcrypt.checkpw(str.encode(old_password), str.encode(user.get_password())):
            raise Exception("Password authentication failed for old password")
        user.set_password(new_password)
        result = self.super_user_repo.update_password(super_user_id, user.get_password())
        if not result.get_status():
            raise Exception("Failed to update password")
        return user

    def __build_super_user_obj(self, data) -> SuperUser:
        """ Build SuperUser object
        Args:
            data: Data for creating object
                (int) id:                Super user ID
                (int) user_status_id:    User status ID
                (str) uuid:              Super user UUID
                (str) username:          Super user username
                (str) first_name:        Super user first name
                (str) last_name:         Super user last name
                (str) password:          Super user password encrypted
                (str) email:             Super user email
                (str) phone:             Super user phone
                (datetime) created_date: Super user created date
        Returns:
            SuperUser
        """
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

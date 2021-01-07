from datetime import datetime
import bcrypt
from modules.User.objects.UserStatus import UserStatus


class User:
    """ Object for basic user attributes that can be extended
    """

    def __init__(self):
        """ Constructor for User
        """

        self.id = None
        self.user_status = None
        self.uuid = None
        self.username = None
        self.first_name = None
        self.last_name = None
        self.password = None
        self.email = None
        self.phone = None
        self.created_date = None

    def set_id(self, user_id: int):
        self.id = user_id

    def get_id(self) -> int:
        return self.id

    def set_user_status(self, user_status: UserStatus):
        self.user_status = user_status

    def get_user_status(self) -> UserStatus:
        return self.user_status

    def set_uuid(self, uuid: str):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_username(self, username: str):
        self.username = username

    def get_username(self) -> str:
        return self.username

    def set_first_name(self, first_name: str):
        self.first_name = first_name

    def get_first_name(self) -> str:
        return self.first_name

    def set_last_name(self, last_name: str):
        self.last_name = last_name

    def get_last_name(self) -> str:
        return self.last_name

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt(14)).decode()

    def set_password_encrypted(self, password: str):
        self.password = password

    def get_password(self) -> str:
        return self.password

    def set_email(self, email: str):
        self.email = email

    def get_email(self) -> str:
        return self.email

    def set_phone(self, phone: int):
        self.phone = phone

    def get_phone(self) -> int:
        return self.phone

    def set_created_date(self, created_date: datetime):
        self.created_date = created_date

    def get_created_date(self) -> datetime:
        return self.created_date

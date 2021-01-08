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
        """ Set ID
        Args:
            (int) user_id: User ID
        """
        self.id = user_id

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.id

    def set_user_status(self, user_status: UserStatus):
        """ Set user status
        Args:
            (int) user_status: User status object
        """
        self.user_status = user_status

    def get_user_status(self) -> UserStatus:
        """ Get user status
        Returns:
            UserStatus
        """
        return self.user_status

    def set_uuid(self, uuid: str):
        """ Set UUID
        Args:
            (str) uuid: User UUID
        """
        self.uuid = uuid

    def get_uuid(self) -> str:
        """ Get UUID
        Returns:
            str
        """
        return self.uuid

    def set_username(self, username: str):
        """ Set username
        Args:
            (str) username: User username
        """
        self.username = username

    def get_username(self) -> str:
        """ Get username
        Returns:
            str
        """
        return self.username

    def set_first_name(self, first_name: str):
        """ Set first name
        Args:
            (str) first_name: User first name
        """
        self.first_name = first_name

    def get_first_name(self) -> str:
        """ Get first name
        Returns:
            str
        """
        return self.first_name

    def set_last_name(self, last_name: str):
        """ Set last name
        Args:
            (str) last_name: User last name
        """
        self.last_name = last_name

    def get_last_name(self) -> str:
        """ Get last name
        Returns:
            str
        """
        return self.last_name

    def set_password(self, password: str):
        """ Set password
        Args:
            (str) password: User password unencrypted
        """
        self.password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt(14)).decode()

    def set_password_encrypted(self, password: str):
        """ Set password encrypted
        Args:
            (str) password: User password encrypted
        """
        self.password = password

    def get_password(self) -> str:
        """ Get password encrypted
        Returns:
            str
        """
        return self.password

    def set_email(self, email: str):
        """ Set email
        Args:
            (str) email: User email
        """
        self.email = email

    def get_email(self) -> str:
        """ Get email
        Returns:
            str
        """
        return self.email

    def set_phone(self, phone: str):
        """ Set phone
        Args:
            (str) phone: User phone
        """
        self.phone = phone

    def get_phone(self) -> str:
        """ Get phone
        Returns:
            str
        """
        return self.phone

    def set_created_date(self, created_date: datetime):
        """ Set created date
        Args:
            (datetime) created_date: User created date
        """
        self.created_date = created_date

    def get_created_date(self) -> datetime:
        """ Get created date
        Returns:
            datetime
        """
        return self.created_date

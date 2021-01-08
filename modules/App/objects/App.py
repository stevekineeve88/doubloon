from datetime import datetime


class App:
    """ Object for app attributes
    """

    def __init__(self):
        """ Construction for App
        """
        self.__id = None
        self.__uuid = None
        self.__name = None
        self.__api_key = None
        self.__api_key_unencrypted = None
        self.__created_date = None

    def set_id(self, app_id: int):
        """ Set App ID
        Args:
            (int) app_id:
        """
        self.__id = app_id

    def get_id(self) -> int:
        """ Get App ID
        Returns:
            int
        """
        return self.__id

    def set_uuid(self, uuid: str):
        """ Set App UUID
        Args:
            (str) uuid:
        """
        self.__uuid = uuid

    def get_uuid(self) -> str:
        """ Get App UUID
        Returns:
            str
        """
        return self.__uuid

    def set_name(self, name: str):
        """ Set App Name
        Args:
            (str) name:
        """
        self.__name = name

    def get_name(self) -> str:
        """ Get App Name
        Returns:
            str
        """
        return self.__name

    def set_api_key(self, api_key: str):
        """ Set App API Key
        Args:
            (str) api_key:
        """
        self.__api_key = api_key

    def get_api_key(self) -> str:
        """ Get App API Key
        Returns:
            str
        """
        return self.__api_key

    def set_created_date(self, created_date: datetime):
        """ Set App Created Date
        Args:
            (datetime) created_date:
        """
        self.__created_date = created_date

    def get_created_date(self) -> datetime:
        """ Get App Created Date
        Returns:
            datetime
        """
        return self.__created_date

    def to_dict(self) -> dict:
        """ Convert object to dictionary
        Returns:
            dict
        """
        return {
            "id": self.get_id(),
            "uuid": self.get_uuid(),
            "name": self.get_name(),
            "api_key": self.get_api_key(),
            "created_date": self.get_created_date()
        }

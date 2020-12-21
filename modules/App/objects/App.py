from datetime import datetime


class App:
    def __init__(self):
        self.__id = None
        self.__uuid = None
        self.__name = None
        self.__api_key = None
        self.__api_key_unencrypted = None
        self.__created_date = None

    def set_id(self, app_id: int):
        self.__id = app_id

    def get_id(self) -> int:
        return self.__id

    def set_uuid(self, uuid: str):
        self.__uuid = uuid

    def get_uuid(self) -> str:
        return self.__uuid

    def set_name(self, name: str):
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_api_key(self, api_key: str):
        self.__api_key = api_key

    def get_api_key(self) -> str:
        return self.__api_key

    def set_created_date(self, created_date: datetime):
        self.__created_date = created_date

    def get_created_date(self) -> datetime:
        return self.__created_date

    def to_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "uuid": self.get_uuid(),
            "name": self.get_name(),
            "api_key": self.get_api_key(),
            "created_date": self.get_created_date()
        }

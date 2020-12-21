import os


class APIConfig:
    def __init__(self):
        self.doubloon_access_id = os.environ["DOUBLOON_ACCESS_ID"]
        self.doubloon_api_key = os.environ["DOUBLOON_API_KEY"]

    def is_doubloon_access_id(self, compare: str) -> bool:
        return compare == self.doubloon_access_id

    def is_doubloon_api_key(self, compare: str) -> bool:
        return compare == self.doubloon_api_key

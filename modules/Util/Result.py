class Result:
    def __init__(self):
        self.status = True
        self.data = []
        self.insert_id = None
        self.message = None
        self.metadata = {}

    def set_status(self, status: bool):
        self.status = status

    def get_status(self) -> bool:
        return self.status

    def set_data(self, data: list):
        self.data = data

    def get_data(self):
        return self.data

    def set_insert_id(self, insert_id):
        self.insert_id = insert_id

    def get_insert_id(self):
        return self.insert_id

    def get_message(self) -> str:
        return self.message

    def set_message(self, message: str):
        self.message = message

    def set_metadata(self, metadata: dict):
        self.metadata = metadata

    def set_metadata_attribute(self, key: str, value):
        self.metadata[key] = value

    def get_metadata(self) -> dict:
        return self.metadata

    def get_metadata_attribute(self, key: str):
        return self.metadata[key]

class RowMock:
    def __init__(self, attributes: dict):
        self.attributes = attributes

    def get(self, key):
        return self.attributes[key]

    def get_all(self):
        return self.attributes

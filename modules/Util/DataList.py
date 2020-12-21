class DataList:
    def __init__(self, items: list, item_id: str = "id", attribute: str = "const"):
        self.items = {}
        self.id_map = {}
        for item in items:
            attribute_key = item[attribute]
            id_key = item[item_id]
            self.items[attribute_key] = item
            self.id_map[id_key] = attribute_key

    def __getattr__(self, attribute: str):
        return self.items[attribute]

    def get(self, item_id):
        return self.items[self.id_map[item_id]]

    def get_all(self):
        return self.items

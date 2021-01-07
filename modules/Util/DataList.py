class DataList:
    """ Class for handling generic object lists as dictionaries with object values
    """

    def __init__(self, items: list, item_id: str = "id", attribute: str = "const"):
        """ Constructor for DataList
        Args:
            (list) items:       List of object items
            (str) item_id:      ID key
            (str) attribute:    Constant attribute key
        """
        self.items = {}
        self.id_map = {}
        item: dict
        for item in items:
            attribute_key = item[attribute]
            id_key = item[item_id]
            self.items[attribute_key] = item
            self.id_map[id_key] = attribute_key

    def __getattr__(self, attribute: str):
        """ Get item by constant attribute
        Args:
            (str) attribute: Constant attribute
        Returns:
            any
        """
        return self.items[attribute]

    def get(self, item_id):
        """ Get item by ID key
        Args:
            item_id: ID Key
        Returns:
            any
        """
        return self.items[self.id_map[item_id]]

    def get_all(self) -> dict:
        """ Get all items
        Returns:
            dict
        """
        return self.items

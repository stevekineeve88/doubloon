class Result:
    """ Class for a generic result of a function
    """

    def __init__(self):
        """ Constructor for Result
        """
        self.status = True
        self.data = []
        self.insert_id = None
        self.message = None
        self.metadata = {}

    def set_status(self, status: bool):
        """ Set status
        Args:
            (bool) status:
        """
        self.status = status

    def get_status(self) -> bool:
        """ Get status
        Returns:
            bool
        """
        return self.status

    def set_data(self, data: list):
        """ Set data
        Args:
            (list) data: Data items
        """
        self.data = data

    def get_data(self) -> list:
        """ Get data
        Returns:
            list
        """
        return self.data

    def set_insert_id(self, insert_id):
        """ Set insert ID
        Args:
            (any) insert_id: Insert ID from some operation
        """
        self.insert_id = insert_id

    def get_insert_id(self):
        """ Get insert ID
        Returns:
            any
        """
        return self.insert_id

    def get_message(self) -> str:
        """ Get message
        Returns:
            str
        """
        return self.message

    def set_message(self, message: str):
        """ Set message
        Args:
            (str) message:
        """
        self.message = message

    def set_metadata(self, metadata: dict):
        """ Set metadata
        Args:
            (dict) metadata:
        """
        self.metadata = metadata

    def set_metadata_attribute(self, key: str, value):
        """ Set metadata attribute
        Args:
            (str) key:      Metadata attribute key
            (any) value:    Value for key
        """
        self.metadata[key] = value

    def get_metadata(self) -> dict:
        """ Get metadata
        Returns:
            dict
        """
        return self.metadata

    def get_metadata_attribute(self, key: str):
        """ Get metadata attribute value
        Args:
            (str) key: Metadata attribute key to fetch by
        Returns:
            any
        """
        return self.metadata[key]

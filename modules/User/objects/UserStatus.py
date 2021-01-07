class UserStatus:
    """ Object for user status attributes
    """

    def __init__(self, status_id: int, const: str, description: str):
        """ Constructor for UserStatus
        Args:
            (int) status_id:    User status ID
            (str) const:        User status constant
            (str) description:  User status description
        """
        self.id = status_id
        self.const = const
        self.description = description

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.id

    def get_const(self) -> str:
        """ Get constant
        Returns:
            str
        """
        return self.const

    def get_description(self) -> str:
        """ Get description
        Returns:
            str
        """
        return self.description

    def to_dict(self) -> dict:
        """ Convert object to dictionary
        Returns:
            dict
        """
        return {
            "id": self.get_id(),
            "const": self.get_const(),
            "description": self.get_description()
        }

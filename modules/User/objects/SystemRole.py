class SystemRole:
    """ Object for system role attributes
    """

    def __init__(self, system_role_id: int, const: str, description: str):
        """ Constructor for SystemRole
        Args:
            (int) system_role_id: System role ID
            (str) const:          System role constant
            (str) description:    System role description
        """
        self.id = system_role_id
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

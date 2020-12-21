class SystemRole:
    def __init__(self, system_status_id: int, const: str, description: str):
        self.id = system_status_id
        self.const = const
        self.description = description

    def get_id(self) -> int:
        return self.id

    def get_const(self) -> str:
        return self.const

    def get_description(self) -> str:
        return self.description

    def to_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "const": self.get_const(),
            "description": self.get_description()
        }

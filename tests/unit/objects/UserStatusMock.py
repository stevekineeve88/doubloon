from tests.unit.objects.RowMock import RowMock


class UserStatusMock(RowMock):
    def __init__(self, **kwargs):
        super().__init__({
            "id": kwargs.get("id"),
            "const": kwargs.get("const"),
            "description": kwargs.get("description")
        })

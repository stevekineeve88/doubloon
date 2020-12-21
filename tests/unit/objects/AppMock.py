from tests.unit.objects.RowMock import RowMock


class AppMock(RowMock):
    def __init__(self, **kwargs):
        super().__init__({
            "id": kwargs.get("id"),
            "api_key": kwargs.get("api_key"),
            "uuid": kwargs.get("uuid"),
            "name": kwargs.get("name"),
            "created_date": kwargs.get("created_date"),
        })

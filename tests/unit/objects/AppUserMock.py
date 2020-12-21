from tests.unit.objects.RowMock import RowMock


class AppUserMock(RowMock):
    def __init__(self, **kwargs):
        super().__init__({
            "id": kwargs.get("id") or None,
            "user_status_id": kwargs.get("user_status_id"),
            "system_role_id": kwargs.get("system_role_id"),
            "app_id": kwargs.get("app_id"),
            "app_uuid": kwargs.get("app_uuid"),
            "uuid": kwargs.get("uuid") or None,
            "username": kwargs.get("username") or None,
            "first_name": kwargs.get("first_name") or None,
            "last_name": kwargs.get("last_name") or None,
            "password": kwargs.get("password") or None,
            "email": kwargs.get("email") or None,
            "phone": kwargs.get("phone") or None,
            "created_date": kwargs.get("created_date") or None
        })

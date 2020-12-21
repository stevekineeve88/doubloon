from modules.App.objects.App import App
from modules.User.objects.AppUser import AppUser
from modules.User.objects.SuperUser import SuperUser
from tests.unit.objects.AppMock import AppMock
from tests.unit.objects.AppUserMock import AppUserMock
from tests.unit.objects.SuperUserMock import SuperUserMock


class MockGenerator:
    @staticmethod
    def create_super_user_mock(user_obj: SuperUser, user_id: int, uuid: str, user_status_id: int):
        return SuperUserMock(
            id=user_id,
            uuid=uuid,
            user_status_id=user_status_id,
            username=user_obj.get_username(),
            first_name=user_obj.get_first_name(),
            last_name=user_obj.get_last_name(),
            email=user_obj.get_email(),
            phone=user_obj.get_phone(),
            password=user_obj.get_password(),
            created_date=user_obj.get_created_date()
        )

    @staticmethod
    def create_app_mock(app_obj: App):
        return AppMock(
            id=app_obj.get_id(),
            api_key=app_obj.get_api_key(),
            uuid=app_obj.get_uuid(),
            name=app_obj.get_name(),
            created_date=app_obj.get_created_date()
        )

    @staticmethod
    def create_app_user_mock(user_obj: AppUser,
                             user_id: int,
                             uuid: str,
                             user_status_id: int,
                             system_role_id: int,
                             app_id: int,
                             app_uuid: str):
        return AppUserMock(
            id=user_id,
            uuid=uuid,
            user_status_id=user_status_id,
            system_role_id=system_role_id,
            app_id=app_id,
            app_uuid=app_uuid,
            username=user_obj.get_username(),
            first_name=user_obj.get_first_name(),
            last_name=user_obj.get_last_name(),
            email=user_obj.get_email(),
            phone=user_obj.get_phone(),
            password=user_obj.get_password(),
            created_date=user_obj.get_created_date()
        )

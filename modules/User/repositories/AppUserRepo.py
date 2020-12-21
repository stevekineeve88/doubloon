from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class AppUserRepo:
    def __init__(self, **kwargs):
        self.db_connection = kwargs.get("db_connection") or DBConnection()

    def insert(self, data) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('INSERT INTO "User_AppUsers" '
                           '('
                                'first_name, '
                                'last_name, '
                                'user_status_id, '
                                'system_role_id, '
                                'username, '
                                'password, '
                                'email, '
                                'phone, '
                                'app_id, '
                                'app_uuid'
                           ') '
                           'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                           (
                               data["first_name"],
                               data["last_name"],
                               data["user_status_id"],
                               data["system_role_id"],
                               data["username"],
                               data["password"],
                               data["email"],
                               data["phone"],
                               data["app_id"],
                               data["app_uuid"])
                           )
            user_id = cursor.fetchone()["id"]
            self.db_connection.get_connection().commit()
            result.set_insert_id(user_id)
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            cursor.close()

    def load(self, app_user_id: int) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('SELECT '
                           '"User_AppUsers".id, '
                           '"User_AppUsers".user_status_id, '
                           '"User_AppUsers".system_role_id, '
                           '"User_AppUsers".uuid, '
                           '"User_AppUsers".username, '
                           '"User_AppUsers".first_name, '
                           '"User_AppUsers".last_name, '
                           '"User_AppUsers".email, '
                           '"User_AppUsers".password, '
                           '"User_AppUsers".phone, '
                           '"User_AppUsers".app_id, '
                           '"User_AppUsers".app_uuid, '
                           '"User_AppUsers".created_date '
                           'FROM "User_AppUsers"'
                           'WHERE "User_AppUsers".id = %s',
                           (
                               app_user_id,
                           ))
            data = cursor.fetchall()
            cursor.close()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result
        finally:
            cursor.close()

    def search_app_users(self,
                         app_name: str,
                         search: str,
                         limit: int,
                         offset: int,
                         user_status_id: int,
                         order: dict
                         ) -> Result:
        pass

    def search_all(self, search: str, limit: int, offset: int, user_status_id: int, order: dict) -> Result:
        pass

    def update_status(self, app_user_id: int, user_status_id: int) -> Result:
        pass

    def update(self, app_user_id: int, data: dict) -> Result:
        pass

    def update_password(self, app_user_id: int, new_password: str) -> Result:
        pass

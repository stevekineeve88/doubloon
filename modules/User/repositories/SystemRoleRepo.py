from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class SystemRoleRepo:
    def __init__(self, **kwargs):
        self.db_connection = kwargs.get("db_connection") or DBConnection()

    def load_all(self) -> Result:
        result = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute('SELECT '
                           '"System_Roles".id, '
                           '"System_Roles".const, '
                           '"System_Roles".description '
                           'FROM "System_Roles"'
                           )
            data = cursor.fetchall()
            cursor.close()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result

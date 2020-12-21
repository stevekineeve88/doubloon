from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class UserStatusRepo:
    def __init__(self, **kwargs):
        self.db_connection = kwargs.get("db_connection") or DBConnection()

    def load_all(self) -> Result:
        result = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute('SELECT '
                                '"User_Statuses".id, '
                                '"User_Statuses".const, '
                                '"User_Statuses".description '
                           'FROM "User_Statuses"'
                           )
            data = cursor.fetchall()
            cursor.close()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result

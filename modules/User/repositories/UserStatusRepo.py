from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class UserStatusRepo:
    """ Class for user status database operations
    """

    def __init__(self, **kwargs):
        """ Constructor for UserStatusRepo
        Args:
            **kwargs: Dependencies if needed
                (DBConnection) db_connection
        """
        self.db_connection: DBConnection = kwargs.get("db_connection") or DBConnection()

    def load_all(self) -> Result:
        """ Load all user statuses
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
                '"User_Statuses".id, '
                '"User_Statuses".const, '
                '"User_Statuses".description '
                'FROM "User_Statuses"'
            )
            data = cursor.fetchall()
            result.set_data(data)
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            cursor.close()
        return result

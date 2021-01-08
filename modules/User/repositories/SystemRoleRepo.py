from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class SystemRoleRepo:
    """ Class for system role database operations
    """

    def __init__(self, **kwargs):
        """ Constructor for SystemRoleRepo
        Args:
            **kwargs: Dependencies if needed
                (DBConnection) db_connection
        """
        self.db_connection: DBConnection = kwargs.get("db_connection") or DBConnection()

    def load_all(self) -> Result:
        """ Load all system roles
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
                '"System_Roles".id, '
                '"System_Roles".const, '
                '"System_Roles".description '
                'FROM "System_Roles"'
            )
            data = cursor.fetchall()
            result.set_data(data)
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            cursor.close()
        return result

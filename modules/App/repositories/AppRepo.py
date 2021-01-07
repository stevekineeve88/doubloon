from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class AppRepo:
    """ Class for handling app database operations
    """

    def __init__(self, **kwargs):
        """ Constructor for AppRepo
        Args:
            **kwargs: Dependencies if needed
                (DBConnection) db_connection
        """
        self.db_connection: DBConnection = kwargs.get("db_connection") or DBConnection()

    def create(self, name: str, api_key: str) -> Result:
        """ Create app
        Args:
            (str) name:     App name
            (str) api_key:  App API key
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO "App_Apps" '
                '(name, api_key) '
                'VALUES (%(name)s, %(api_key)s) RETURNING id',
                {
                    "name": name,
                    "api_key": api_key
                }
            )
            app_id = cursor.fetchone()["id"]
            self.db_connection.get_connection().commit()
            result.set_insert_id(app_id)
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()
        return result

    def create_partition(self, app_name: str, app_uuid: str) -> Result:
        """ Create app users partition for app
        Args:
            (str) app_name: App name
            (str) app_uuid: App UUID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                f'CREATE TABLE "{app_name}" '
                'PARTITION OF "User_AppUsers" '
                'FOR VALUES IN(%(app_uuid)s)',
                {
                    "app_uuid": app_uuid
                }
            )
            self.db_connection.get_connection().commit()
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()
        return result

    def load(self, app_id) -> Result:
        """ Load app by app ID
        Args:
            (int) app_id: App ID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
                '"App_Apps".id, '
                '"App_Apps".uuid, '
                '"App_Apps".name, '
                '"App_Apps".api_key, '
                '"App_Apps".created_date '
                'FROM "App_Apps"'
                'WHERE "App_Apps".id = %(id)s',
                {
                    "id": app_id
                }
            )
            data = cursor.fetchall()
            result.set_data(data)
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            cursor.close()
        return result

    def load_by_name(self, app_name: str) -> Result:
        """ Load app by name
        Args:
            (str) app_name: App name
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
                '"App_Apps".id, '
                '"App_Apps".uuid, '
                '"App_Apps".name, '
                '"App_Apps".api_key, '
                '"App_Apps".created_date '
                'FROM "App_Apps"'
                'WHERE "App_Apps".name = %(app_name)s',
                {
                    "app_name": app_name
                }
            )
            data = cursor.fetchall()
            result.set_data(data)
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            cursor.close()
        return result

    def load_by_uuid(self, app_uuid: str) -> Result:
        """ Load app by UUID
        Args:
            (str) app_uuid: App UUID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
                '"App_Apps".id, '
                '"App_Apps".uuid, '
                '"App_Apps".name, '
                '"App_Apps".api_key, '
                '"App_Apps".created_date '
                'FROM "App_Apps"'
                'WHERE "App_Apps".uuid = %(app_uuid)s',
                {
                    "app_uuid": app_uuid
                }
            )
            data = cursor.fetchall()
            result.set_data(data)
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            cursor.close()
        return result

    def delete(self, app_id) -> Result:
        """ Delete app by ID
        Args:
            (int) app_id: App ID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'DELETE FROM "App_Apps" '
                'WHERE "App_Apps".id = %(id)s ',
                {
                    "id": app_id
                }
            )
            self.db_connection.get_connection().commit()
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()
        return result

    def search(self, search: str, limit: int, offset: int, order: dict) -> Result:
        """ Search apps
        Args:
            (str) search: Search string
            (int) limit:  Limit of result
            (int) offset: Offset of result
            (dict) order: Order of results with column key and ASC(1) or DESC(-1)
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            order_by_columns = []
            not_allowed = ["id", "uuid", "api_key"]
            for key, value in order.items():
                if key in not_allowed:
                    raise Exception("Order not allowed")
                order_clause = "ASC" if value > 0 else "DESC"
                order_by_columns.append(f'"App_Apps".{key} {order_clause}')
            order_statement = f'ORDER BY {", ".join(order_by_columns)}' if len(order_by_columns) > 0 else ""
            cursor.execute(
                'SELECT '
                '"App_Apps".id, '
                '"App_Apps".uuid, '
                '"App_Apps".name, '
                '"App_Apps".api_key, '
                '"App_Apps".created_date, '
                'count(*) OVER() AS count '
                'FROM "App_Apps" '
                'WHERE "App_Apps".name LIKE %(search)s '
                f'{order_statement} '
                'LIMIT %(limit)s OFFSET %(offset)s',
                {
                    "search": f'%{search}%',
                    "limit": limit,
                    "offset": offset
                }
            )
            data = cursor.fetchall()
            result.set_data(data)
            result.set_metadata({
                "total_count": data[0]["count"] if len(data) > 0 else 0
            })
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
        finally:
            cursor.close()
        return result

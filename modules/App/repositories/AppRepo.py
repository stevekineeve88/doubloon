from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class AppRepo:
    def __init__(self, **kwargs):
        self.db_connection = kwargs.get("db_connection") or DBConnection()

    def create(self, name: str, api_key: str) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('INSERT INTO "App_Apps" '
                           '(name, api_key) '
                           'VALUES (%s, %s) RETURNING id',
                           (
                               name,
                               api_key)
                           )
            app_id = cursor.fetchone()["id"]
            self.db_connection.get_connection().commit()
            result.set_insert_id(app_id)
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result
        finally:
            cursor.close()

    def create_partition(self, name: str, uuid: str) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(f'CREATE TABLE "{name}" PARTITION OF "User_AppUsers" FOR VALUES IN(%s)', (uuid,))
            self.db_connection.get_connection().commit()
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result
        finally: cursor.close()

    def load(self, app_id) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('SELECT '
                           '"App_Apps".id, '
                           '"App_Apps".uuid, '
                           '"App_Apps".name, '
                           '"App_Apps".api_key, '
                           '"App_Apps".created_date '
                           'FROM "App_Apps"'
                           'WHERE "App_Apps".id = %s',
                           (app_id,))
            data = cursor.fetchall()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result
        finally:
            cursor.close()

    def load_by_name(self, app_name: str) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('SELECT '
                           '"App_Apps".id, '
                           '"App_Apps".uuid, '
                           '"App_Apps".name, '
                           '"App_Apps".api_key, '
                           '"App_Apps".created_date '
                           'FROM "App_Apps"'
                           'WHERE "App_Apps".name = %(app_name)s',
                           {"app_name": app_name})
            data = cursor.fetchall()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result
        finally:
            cursor.close()

    def load_by_uuid(self, app_uuid: str) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('SELECT '
                           '"App_Apps".id, '
                           '"App_Apps".uuid, '
                           '"App_Apps".name, '
                           '"App_Apps".api_key, '
                           '"App_Apps".created_date '
                           'FROM "App_Apps"'
                           'WHERE "App_Apps".uuid = %(app_uuid)s',
                           {"app_uuid": app_uuid})
            data = cursor.fetchall()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result
        finally:
            cursor.close()

    def delete(self, app_id) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('DELETE FROM "App_Apps" '
                           'WHERE "App_Apps".id = %s ',
                           (app_id,))
            self.db_connection.get_connection().commit()
            return result
        except Exception as e:
            result.set_message(str(e))
            result.set_status(False)
            return result
        finally:
            cursor.close()

    def search(self, search: str, limit: int, offset: int, order: dict) -> Result:
        result = Result()
        try:
            order_by_columns = []
            not_ordered = ["id", "uuid", "api_key"]
            for key, value in order.items():
                if key in not_ordered:
                    raise Exception("Order not allowed")
                order_clause = "ASC" if value > 0 else "DESC"
                order_by_columns.append(f'"App_Apps".{key} {order_clause}')
            order_statement = f'ORDER BY {", ".join(order_by_columns)}' if len(order_by_columns) > 0 else ""
            cursor = self.db_connection.get_cursor()
            cursor.execute('SELECT '
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
                           })
            data = cursor.fetchall()
            cursor.close()
            result.set_data(data)
            result.set_metadata({
                "total_count": data[0]["count"] if len(data) > 0 else 0
            })
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result

    def update_api_key(self, app_id: int, api_key: str) -> Result:
        pass

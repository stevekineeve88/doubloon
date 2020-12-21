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
        pass

    def update_api_key(self, app_id: int, api_key: str) -> Result:
        pass

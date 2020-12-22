from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class SuperUserRepo:
    def __init__(self, **kwargs):
        self.db_connection = kwargs.get("db_connection") or DBConnection()

    def insert(self, data: dict) -> Result:
        result = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute('INSERT INTO "User_SuperUsers" '
                           '(first_name, last_name, user_status_id, username, password, email, phone) '
                           'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id',
                           (
                               data["first_name"],
                               data["last_name"],
                               data["user_status_id"],
                               data["username"],
                               data["password"],
                               data["email"],
                               data["phone"])
                           )
            user_id = cursor.fetchone()["id"]
            self.db_connection.get_connection().commit()
            cursor.close()
            result.set_insert_id(user_id)
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result

    def load(self, user_id: int) -> Result:
        result = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute('SELECT '
                           '"User_SuperUsers".id, '
                           '"User_SuperUsers".uuid, '
                           '"User_SuperUsers".user_status_id, '
                           '"User_SuperUsers".username, '
                           '"User_SuperUsers".first_name, '
                           '"User_SuperUsers".last_name, '
                           '"User_SuperUsers".password, '
                           '"User_SuperUsers".email, '
                           '"User_SuperUsers".phone, '
                           '"User_SuperUsers".created_date '
                           'FROM "User_SuperUsers" '
                           'WHERE "User_SuperUsers".id = %s',
                           (user_id,)
                           )
            data = cursor.fetchall()
            cursor.close()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result

    def load_by_username(self, username: str) -> Result:
        result = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute('SELECT '
                           '"User_SuperUsers".id, '
                           '"User_SuperUsers".uuid, '
                           '"User_SuperUsers".user_status_id, '
                           '"User_SuperUsers".username, '
                           '"User_SuperUsers".first_name, '
                           '"User_SuperUsers".last_name, '
                           '"User_SuperUsers".password, '
                           '"User_SuperUsers".email, '
                           '"User_SuperUsers".phone, '
                           '"User_SuperUsers".created_date '
                           'FROM "User_SuperUsers" '
                           'WHERE "User_SuperUsers".username = %s',
                           (username,)
                           )
            data = cursor.fetchall()
            cursor.close()
            result.set_data(data)
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result

    def search(self, search: str, limit: int, offset: int, status_id: int, order: dict) -> Result:
        # TODO: Implement function
        pass

    def update_status(self, user_id: int, status_id: int) -> Result:
        data_container = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("UPDATE Super_Users "
                           "SET Super_Users.system_status_id = ? "
                           "WHERE Super_Users.id = ?",
                           (status_id, user_id)
                           )
            self.db_connection.get_connection().commit()
            cursor.close()
            return data_container
        except Exception:
            data_container.set_status(False)
            return data_container

    def update(self, user_id: int, data: dict) -> Result:
        data_container = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("UPDATE Super_Users"
                           "SET Super_Users.first_name = ?"
                           "Super_Users.last_name = ?"
                           "Super_Users.email = ?"
                           "Super_Users.phone = ?"
                           "WHERE Super_Users.id = ?",
                           (
                               data["first_name"],
                               data["last_name"],
                               data["email"],
                               data["phone"],
                               user_id)
                           )
            self.db_connection.get_connection().commit()
            cursor.close()
            return data_container
        except Exception:
            data_container.set_status(False)
            return data_container

    def update_password(self, user_id: int, password: str) -> Result:
        data_container = Result()
        try:
            cursor = self.db_connection.get_cursor()
            cursor.execute("UPDATE Super_Users"
                           "SET Super_Users.password = ?"
                           "WHERE Super_Users.id = ?",
                           (password, user_id)
                           )
            self.db_connection.get_connection().commit()
            cursor.close()
            return data_container
        except Exception:
            data_container.set_status(False)
            return data_container

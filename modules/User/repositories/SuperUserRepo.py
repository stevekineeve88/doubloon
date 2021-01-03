from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class SuperUserRepo:
    def __init__(self, **kwargs):
        self.db_connection = kwargs.get("db_connection") or DBConnection()

    def insert(self, data: dict) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
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
            result.set_insert_id(user_id)
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()

    def load(self, user_id: int) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
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
            result.set_data(data)
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            cursor.close()

    def load_by_username(self, username: str) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
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
            result.set_data(data)
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            cursor.close()

    def search(self, search: str, limit: int, offset: int, user_status_id: int, order: dict) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            order_by_columns = []
            not_ordered = ["id", "uuid", "user_status_id", "password"]
            for key, value in order.items():
                if key in not_ordered:
                    raise Exception("Order not allowed")
                order_clause = "ASC" if value > 0 else "DESC"
                order_by_columns.append(f'"User_SuperUsers".{key} {order_clause}')
            order_statement = f'ORDER BY {", ".join(order_by_columns)}' if len(order_by_columns) > 0 else ""
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
                           '"User_SuperUsers".created_date, '
                           'count(*) OVER() AS count '
                           'FROM "User_SuperUsers" '
                           'WHERE ('
                                '"User_SuperUsers".username LIKE %(search)s '
                                'OR "User_SuperUsers".first_name LIKE %(search)s '
                                'OR "User_SuperUsers".last_name LIKE %(search)s '
                                'OR "User_SuperUsers".email LIKE %(search)s'
                           ') '
                           'AND "User_SuperUsers".user_status_id = %(user_status_id)s'
                           f'{order_statement} '
                           'LIMIT %(limit)s OFFSET %(offset)s',
                           {
                               "search": f'%{search}%',
                               "user_status_id": user_status_id,
                               "limit": limit,
                               "offset": offset
                           })
            data = cursor.fetchall()
            result.set_data(data)
            result.set_metadata({
                "total_count": data[0]["count"] if len(data) > 0 else 0
            })
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            cursor.close()

    def update_status(self, user_id: int, user_status_id: int) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('UPDATE "User_SuperUsers" '
                           'SET user_status_id = %(user_status_id)s '
                           'WHERE id = %(id)s',
                           {
                               "user_status_id": user_status_id,
                               "id": user_id
                           }
                           )
            self.db_connection.get_connection().commit()
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()

    def update(self, user_id: int, data: dict) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            data["id"] = user_id
            cursor.execute('UPDATE "User_SuperUsers" '
                            'SET first_name = %(first_name)s, '
                            'last_name = %(last_name)s, '
                            'email = %(email)s, '
                            'phone = %(phone)s '
                           'WHERE id = %(id)s',
                           data
                           )
            self.db_connection.get_connection().commit()
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()

    def update_password(self, super_user_id: int, password: str) -> Result:
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute('UPDATE "User_SuperUsers" '
                           'SET password = %(password)s '
                           'WHERE id = %(id)s',
                           {
                               "password": password,
                               "id": super_user_id
                           })
            self.db_connection.get_connection().commit()
            return result
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
            return result
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()

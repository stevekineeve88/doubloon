from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class SuperUserRepo:
    """ Class for super user database operations
    """

    def __init__(self, **kwargs):
        """ Constructor for SuperUserRepo
        Args:
            **kwargs: Dependencies if needed
                (DBConnection) db_connection
        """
        self.db_connection: DBConnection = kwargs.get("db_connection") or DBConnection()

    def insert(self, data: dict) -> Result:
        """ Insert super user
        Args:
            (dict) data: Data for insert
                (str) first_name:           User first name
                (str) last_name:            User last name
                (int) user_status_id:       User status ID
                (str) username:             User username
                (str) password:             User password encrypted
                (str) email:                User email
                (str) phone:                User phone
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO "User_SuperUsers" ('
                'first_name, '
                'last_name, '
                'user_status_id, '
                'username, '
                'password, '
                'email, '
                'phone'
                ') '
                'VALUES ('
                '%(first_name)s, '
                '%(last_name)s, '
                '%(user_status_id)s, '
                '%(username)s, '
                '%(password)s, '
                '%(email)s, '
                '%(phone)s) RETURNING id',
                data
            )
            user_id = cursor.fetchone()["id"]
            self.db_connection.get_connection().commit()
            result.set_insert_id(user_id)
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()
        return result

    def load(self, user_id: int) -> Result:
        """ Load by ID
        Args:
            (int) user_id: Super user ID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
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
                'WHERE "User_SuperUsers".id = %(id)s',
                {
                    "id": user_id
                }
            )
            data = cursor.fetchall()
            result.set_data(data)
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
        finally:
            cursor.close()
        return result

    def load_by_username(self, username: str) -> Result:
        """ Load by username
        Args:
            (str) username: Super user username
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
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
                'WHERE "User_SuperUsers".username = %(username)s',
                {
                    "username": username
                }
            )
            data = cursor.fetchall()
            result.set_data(data)
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
        finally:
            cursor.close()
        return result

    def search(
            self,
            search: str,
            limit: int,
            offset: int,
            user_status_id: int,
            order: dict
    ) -> Result:
        """ Search super users
        Args:
            (str) search:           Search string
            (int) limit:            Limit of result
            (int) offset:           Offset of result
            (int) user_status_id:   User status ID to partition by
            (dict) order:           Order with column key and ASC(1) or DESC(-1)
        Returns:
            Result
        """
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
            cursor.execute(
                'SELECT '
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

    def update_status(self, user_id: int, user_status_id: int) -> Result:
        """ Update status by ID
        Args:
            (int) user_id:          Super user ID
            (int) user_status_id:   User status ID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'UPDATE "User_SuperUsers" '
                'SET user_status_id = %(user_status_id)s '
                'WHERE id = %(id)s',
                {
                    "user_status_id": user_status_id,
                    "id": user_id
                }
            )
            self.db_connection.get_connection().commit()
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()
        return result

    def update(self, user_id: int, data: dict) -> Result:
        """ Update user by ID
        Args:
            (int) user_id:  Super user ID
            (dict) data:    Data to update
                (str) first_name:   Super user first name
                (str) last_name:    Super user last name
                (str) email:        Super user email
                (str) phone:        Super user phone
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            data["id"] = user_id
            cursor.execute(
                'UPDATE "User_SuperUsers" '
                'SET first_name = %(first_name)s, '
                'last_name = %(last_name)s, '
                'email = %(email)s, '
                'phone = %(phone)s '
                'WHERE id = %(id)s',
                data
            )
            self.db_connection.get_connection().commit()
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()
        return result

    def update_password(self, user_id: int, password: str) -> Result:
        """ Update password by ID
        Args:
            (int) user_id:  Super user ID
            (str) password: Password to update encrypted
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'UPDATE "User_SuperUsers" '
                'SET password = %(password)s '
                'WHERE id = %(id)s',
                {
                    "password": password,
                    "id": user_id
                }
            )
            self.db_connection.get_connection().commit()
        except Exception as e:
            result.set_status(False)
            result.set_message(str(e))
        finally:
            self.db_connection.get_connection().rollback()
            cursor.close()
        return result

from modules.Util.DBConnection import DBConnection
from modules.Util.Result import Result


class AppUserRepo:
    """ Class for handling app user database operations
    """

    def __init__(self, **kwargs):
        """ Constructor for AppUserRepo
        Args:
            **kwargs: Dependencies if needed
                (DBConnection) db_connection
        """
        self.db_connection: DBConnection = kwargs.get("db_connection") or DBConnection()

    def insert(self, data) -> Result:
        """ Insert an app user
        Args:
            (dict) data: Data for insert
                (str) first_name:           User first name
                (str) last_name:            User last name
                (int) user_status_id:       User status ID
                (int) system_role_id:       System role
                (str) username:             User username
                (str) password:             User password encrypted
                (str) email:                User email
                (str) phone:                User phone
                (str) app_id:               App ID
                (str) app_uuid:             App UUID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO "User_AppUsers" ('
                'first_name, '
                'last_name, '
                'user_status_id, '
                'system_role_id, '
                'username, '
                'password, '
                'email, '
                'phone, '
                'app_id, '
                'app_uuid'
                ') '
                'VALUES ('
                '%(first_name)s, '
                '%(last_name)s, '
                '%(user_status_id)s, '
                '%(system_role_id)s, '
                '%(username)s, '
                '%(password)s, '
                '%(email)s, '
                '%(phone)s, '
                '%(app_id)s, '
                '%(app_uuid)s) RETURNING id',
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
        """ Load app user by ID
        Args:
            (int) user_id: App user ID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
                '"User_AppUsers".id, '
                '"User_AppUsers".user_status_id, '
                '"User_AppUsers".system_role_id, '
                '"User_AppUsers".uuid, '
                '"User_AppUsers".username, '
                '"User_AppUsers".first_name, '
                '"User_AppUsers".last_name, '
                '"User_AppUsers".email, '
                '"User_AppUsers".password, '
                '"User_AppUsers".phone, '
                '"User_AppUsers".app_id, '
                '"User_AppUsers".app_uuid, '
                '"User_AppUsers".created_date '
                'FROM "User_AppUsers"'
                'WHERE "User_AppUsers".id = %(id)s',
                {
                    "id": user_id,
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

    def load_by_username(self, username: str, app_id: int) -> Result:
        """ Load app user by username
        Args:
            (str) username: App user username
            (int) app_id:   App ID to partition by
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'SELECT '
                '"User_AppUsers".id, '
                '"User_AppUsers".user_status_id, '
                '"User_AppUsers".system_role_id, '
                '"User_AppUsers".uuid, '
                '"User_AppUsers".username, '
                '"User_AppUsers".first_name, '
                '"User_AppUsers".last_name, '
                '"User_AppUsers".email, '
                '"User_AppUsers".password, '
                '"User_AppUsers".phone, '
                '"User_AppUsers".app_id, '
                '"User_AppUsers".app_uuid, '
                '"User_AppUsers".created_date '
                'FROM "User_AppUsers" '
                'WHERE "User_AppUsers".username = %(username)s '
                'AND "User_AppUsers".app_id = %(app_id)s',
                {
                    "username": username,
                    "app_id": app_id
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

    def search_app_users(
            self,
            app_name: str,
            search: str,
            limit: int,
            offset: int,
            user_status_id: int,
            order: dict
    ) -> Result:
        """ Search app users by app
        Args:
            (str) app_name:         App name to partition by
            (str) search:           Search string
            (int) limit:            Limit of result
            (int) offset:           Offset of result
            (int) user_status_id:   User status ID to partition by
            (dict) order:           Order with column key and ASC(1) and DESC(-1)
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            order_by_columns = []
            not_ordered = ["id", "uuid", "user_status_id", "password", "system_role_id", "app_id", "app_uuid"]
            for key, value in order.items():
                if key in not_ordered:
                    raise Exception("Order not allowed")
                order_clause = "ASC" if value > 0 else "DESC"
                order_by_columns.append(f'"{app_name}".{key} {order_clause}')
            order_statement = f'ORDER BY {", ".join(order_by_columns)}' if len(order_by_columns) > 0 else ""
            cursor.execute(
                'SELECT '
                f'"{app_name}".id, '
                f'"{app_name}".uuid, '
                f'"{app_name}".user_status_id, '
                f'"{app_name}".system_role_id, '
                f'"{app_name}".username, '
                f'"{app_name}".first_name, '
                f'"{app_name}".last_name, '
                f'"{app_name}".password, '
                f'"{app_name}".email, '
                f'"{app_name}".phone, '
                f'"{app_name}".created_date, '
                'count(*) OVER() AS count '
                f'FROM {app_name} '
                'WHERE ('
                f'"{app_name}".username LIKE %(search)s '
                f'OR "{app_name}".first_name LIKE %(search)s '
                f'OR "{app_name}".last_name LIKE %(search)s '
                f'OR "{app_name}".email LIKE %(search)s'
                ') '
                f'AND "{app_name}".user_status_id = %(user_status_id)s'
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
            (int) user_id:            App user ID
            (int) user_status_id:     User status ID
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'UPDATE "User_AppUsers" '
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
            (int) user_id:     App user ID
            (dict) data:       Data to update
                (str) first_name:   App user first name
                (str) last_name:    App user last name
                (str) email:        App user email
                (str) phone:        App user phone
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            data["id"] = user_id
            cursor.execute(
                'UPDATE "User_AppUsers" '
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
            (int) user_id:        App user ID
            (str) password:       New password encrypted
        Returns:
            Result
        """
        result = Result()
        cursor = self.db_connection.get_cursor()
        try:
            cursor.execute(
                'UPDATE "User_AppUsers" '
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

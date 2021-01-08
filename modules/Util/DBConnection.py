import os
import psycopg2
import psycopg2.extras


class DBConnection:
    """ Class for handling database connection to postgres
    """

    def __init__(self, **kwargs):
        """ Constructor for DBConnection
        Args:
            **kwargs: Dependencies if needed
                (str) host:     DB host
                (int) port:     DB port
                (str) database: Database name
                (str) user:     DB user
                (str) password: DB password
        """
        self.conn = psycopg2.connect(
            host=kwargs.get("host") or os.environ["POSTGRES_HOST"],
            port=kwargs.get("port") or os.environ["POSTGRES_PORT"],
            database=kwargs.get("database") or os.environ["POSTGRES_DB"],
            user=kwargs.get("user") or os.environ["POSTGRES_USER"],
            password=kwargs.get("password") or os.environ["POSTGRES_PASS"],
        )

    def get_connection(self):
        """ Get DB connection
        Returns:
            DB Connection
        """
        return self.conn

    def get_cursor(self):
        """ Get DB connection cursor
        Returns:
            DB connection cursor
        """
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

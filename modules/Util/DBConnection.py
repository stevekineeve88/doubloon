import os
import psycopg2
import psycopg2.extras


class DBConnection:
    def __init__(self, **kwargs):
        self.conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASS"],
        )

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

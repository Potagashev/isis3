import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class PSQLConnection:

    def __enter__(self):
        self.conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='db',
            port=5432
        )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise


def get_posts() -> list:
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = "SELECT title, author, content FROM posts"
        cursor.execute(query)
        try:
            continents = cursor.fetchall()
        except TypeError:
            return []
        return continents


def add_post(title: str, author: str, content: str):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = f"INSERT INTO posts (id, title, author, content) " \
                f"VALUES (DEFAULT, '{title}', '{author}', '{content}');"
        cursor.execute(query)


def create_posts_table():
    with PSQLConnection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            "select exists("
                "select * from information_schema.tables where table_name=%s"
            ")", ('posts',)
        )
        is_table_exists = cursor.fetchone()[0]
        if not is_table_exists:
            query = """
                CREATE TABLE posts
                    (
                        id SERIAL PRIMARY KEY,
                        title CHARACTER VARYING(30) NOT NULL,
                        author CHARACTER VARYING(30) NOT NULL,
                        content CHARACTER VARYING(1000) NOT NULL
                    );
            """
            cursor.execute(query)

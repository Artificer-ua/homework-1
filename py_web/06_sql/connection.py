from contextlib import contextmanager

import psycopg2
from psycopg2 import Error

from headers import (POSTGRES_DATABASE, POSTGRES_HOST, POSTGRES_PASSWORD,
                     POSTGRES_PORT, POSTGRES_USER)


@contextmanager
def create_connection():
    """create a database connection to a Postgres database"""
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DATABASE,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        yield conn
        conn.commit()
    except Error as err:
        print(err)
        conn.rollback()
    finally:
        conn.close()

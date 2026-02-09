import sqlite3
from contextlib import contextmanager

DB_NAME = 'course_system.db'

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def query_db(query, args=(), one=False):
    with get_db() as conn:
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    with get_db() as conn:
        cur = conn.execute(query, args)
        return cur.lastrowid

import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

pool = pooling.MySQLConnectionPool(
    pool_name="consejo_pool",
    pool_size=5,
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "consejo_departamental"),
)

def get_db():
    """Devuelve una conexión individual desde el pool."""
    return pool.get_connection()

def query(sql, params=None, one=False):
    """SELECT: devuelve lista de dicts (o un dict si one=True)."""
    conn = pool.get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        if one:
            return rows[0] if rows else None
        return rows
    finally:
        conn.close()

def execute(sql, params=None):
    """INSERT/UPDATE/DELETE: devuelve el id insertado."""
    conn = pool.get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

if __name__ == "__main__":
    print(query("SELECT COUNT(*) AS total FROM consejero"))
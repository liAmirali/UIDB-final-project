from db.config import DB_NAME, DB_USER, DB_PASS

import mysql.connector

db_conn = None
db_cursor = None

if db_conn == None or db_cursor == None:
    db_conn = mysql.connector.connect(
        host="localhost",
        user=DB_USER,
        passwd=DB_PASS,
        database=DB_NAME
    )

    db_cursor = db_conn.cursor()

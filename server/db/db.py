from db.config import DB_NAME, DB_USER, DB_PASS

import mysql.connector

my_db = None
db_cursor = None

if my_db == None or db_cursor == None:
    my_db = mysql.connector.connect(
        host="localhost",
        user=DB_USER,
        passwd=DB_PASS,
        database=DB_NAME
    )

    db_cursor = my_db.cursor()

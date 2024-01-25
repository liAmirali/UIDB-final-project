from db.config import DB_NAME, DB_USER, DB_PASS
from src.app import app

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user=DB_USER,
    passwd=DB_PASS
)

print(mydb)
my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE dbproj")

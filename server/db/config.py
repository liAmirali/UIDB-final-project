from dotenv import dotenv_values

env = dotenv_values(".env")

DB_NAME = env.get("DB_NAME")
DB_USER = env.get("DB_USER")
DB_PASS = env.get("DB_PASS")

from views.utils import *
from db.db import db_cursor
from src.app import app
from models.user import User


def show_login_screen():
    clear_screen()
    print_header("Login Page")

    print("1. Login as a Manager")
    print("2. Login as a Customer")
    print("3. Register as a Manager")
    print("4. Register as a Customer")
    print("5. Exit")

    option = read_menu_opt()
    if (option == "1"):
        get_login_credentials("manager")
    elif (option == "2"):
        get_login_credentials("customer")
    elif (option == "3"):
        pass
    elif (option == "4"):
        pass
    elif (option == "5"):
        print("Good bye!")
        return


def get_login_credentials(role):
    username = input("Username: ")
    password = input("Password: ")

    db_cursor.execute(f"SELECT * FROM user WHERE role='{
        role}' AND username='{username}' AND password='{password}'")

    foundUser = db_cursor.fetchone()

    if foundUser is not None:
        print_success("Logged in successfully.")
        user = User(foundUser)
        app.set_logged_in_user(user)
    else:
        print_error("No user found with the given credentials.")

    # TODO: Query username and password
    # TODO: Set the app user object

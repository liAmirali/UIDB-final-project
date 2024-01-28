from views.utils import *
from views.customer_view import show_customer_screen
from views.manager_view import show_manager_screen
from db.db import db_conn, db_cursor
from src.app import app
from models.user import User


def show_login_screen():
    while True:
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
            get_registration_info("manager")
        elif (option == "4"):
            get_registration_info("customer")
        elif (option == "5"):
            print("Good bye!")
            return


def get_login_credentials(role):
    username = input("Username: ")
    password = input("Password: ")

    db_cursor.execute(
        f"SELECT * FROM user WHERE role='{role}' AND username='{username}' AND password='{password}'")

    foundUser = db_cursor.fetchone()

    if foundUser is not None:
        print_success("Logged in successfully.")
        user = User(foundUser)
        app.set_logged_in_user(user)

        wait_on_enter()

        if role == "customer":
            show_customer_screen()
        elif role == "manager":
            show_manager_screen()

    else:
        print_error("No user found with the given credentials.")
        wait_on_enter()


def get_registration_info(role):
    username = input("Username: ")
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")

    address = input("Address: ")
    address2 = input("Address 2: ")
    district = input("District: ")
    postal_code = input("Postal Code: ")
    phone = input("Phone: ")
    location = input("Location: ")
    city = input("City: ")
    country = input("Country: ")

    try:
        insert_addr = "INSERT INTO address (address, address2, district, postal_code, phone, location, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        address_val = (address, address2, district, postal_code,
                       phone, location, city, country)
        db_cursor.execute(insert_addr, address_val)

        address_id = db_cursor.lastrowid

        print("INSERTED ADDRESS ID:", address_id)

        insert_user = "INSERT INTO user (first_name, last_name, username, password, email, address_id, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        user_val = (first_name, last_name, username,
                    password, email, address_id, role)
        db_cursor.execute(insert_user, user_val)

        db_conn.commit()
    except Exception as e:
        db_conn.rollback()
        print_error(f"Error in registration: {str(e)}")

    wait_on_enter()

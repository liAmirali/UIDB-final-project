from views.utils import *
from db.db import db_cursor, db_conn
from src.app import app
from models.user import User


def show_customer_screen():
    while True:
        clear_screen()
        print_header("Customer View")

        print("1. View all shops")
        print("2. View and Edit profile")
        print("3. View films by category")
        print("4. Logout")

        option = read_menu_opt()
        if option == "1":
            get_all_shops()
        elif option == "2":
            get_user_profile()
        elif option == "3":
            pass
        elif option == "4":
            break


def get_all_shops():
    clear_screen()
    print_header("Shop List")

    db_cursor.execute("SELECT * FROM shop")
    all_shops = db_cursor.fetchall()

    print("All Shops")
    for shop in all_shops:
        print(shop)

    wait_on_enter()


def get_user_profile():
    clear_screen()
    print_header("User Profile")

    logged_in_user = app.logged_in_user

    db_cursor.execute(
        f"SELECT * FROM user where user_id={logged_in_user.user_id}")
    foundUser = db_cursor.fetchone()

    if foundUser is None:
        print_error("Couldn't find your data.")
        wait_on_enter()
        return
    else:
        print(foundUser)

    edit_confirmation = input("\n\nDo you want to edit? (Y/N): ")
    if edit_confirmation == "Y" or edit_confirmation == "y":
        show_edit_profile_screen()
    else:
        wait_on_enter()


def show_edit_profile_screen():
    clear_screen()
    print_header("Profile Edit")

    logged_in_user = app.logged_in_user

    print("* Hit enter to keep the old value *")

    print("\n --- User Information ---")

    username = input("Username: ")
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")

    print("\n --- Address ---")

    address = input("Address: ")
    address2 = input("Address 2: ")
    district = input("District: ")
    postal_code = input("Postal Code: ")
    phone = input("Phone: ")
    location = input("Location: ")
    city = input("City: ")
    country = input("Country: ")

    update_user_query = f"""UPDATE user
    SET
        username = {'"' + username + '"' if username != "" else 'username'},
        password = {'"' + password + '"' if password != "" else 'password'},
        first_name = {'"' + first_name +
                      '"' if first_name != "" else 'first_name'},
        last_name = {'"' + last_name +
                     '"' if last_name != "" else 'last_name'},
        email = {'"' + email + '"' if email != "" else 'email'}
    WHERE
        user_id = {logged_in_user.user_id}"""

    print("update_user_query:", update_user_query)

    update_address_query = f"""UPDATE address
    SET
        address = {'"' + address + '"' if address != "" else 'address'},
        address2 = {'"' + address2 + '"' if address2 != "" else 'address2'},
        district = {'"' + district + '"' if district != "" else 'district'},
        postal_code = {'"' + postal_code +
                       '"' if postal_code != "" else 'postal_code'},
        phone = {'"' + phone + '"' if phone != "" else 'phone'},
        location = {'"' + location + '"' if location != "" else 'location'},
        city = {'"' + city + '"' if city != "" else 'city'},
        country = {'"' + country + '"' if country != "" else 'country'}
    WHERE
        address_id = {logged_in_user.address_id}"""
    
    print("update_address_query:", update_address_query)

    try:
        db_cursor.execute(update_user_query)
        db_cursor.execute(update_address_query)

        db_conn.commit()

        db_cursor.execute(
            f"SELECT * FROM user WHERE user_id={logged_in_user.user_id}")
        foundUser = db_cursor.fetchone()
        user = User(foundUser)

        print_success("User was edited successfully.")
    except Exception as e:
        db_conn.rollback()

        print_error(f"Error in updating user info: {str(e)}")

    wait_on_enter()

from views.utils import *
from db.db import db_cursor, db_conn
from src.app import app
from models.user import User


def show_customer_screen():
    while True:
        clear_screen()
        print_header("Customer View")

        print(" 1. View all shops")
        print(" 2. View and Edit profile")
        print(" 3. View films by category")
        print(" 4. Search Films")
        print(" 5. Rental Details")
        print(" 6. View Rental History")
        print(" 7. Reserve a Film")
        print(" 8. Rent a Film")
        print(" 9. Return a Rented DVD")
        print("10. Active Rents")
        print("11. Payment Information")
        print("12. Logout")

        option = read_menu_opt()
        if option == "1":
            get_all_shops()
        elif option == "2":
            get_user_profile()
        elif option == "3":
            view_film_list()
        elif option == "4":
            search_films()
        elif option == "5":
            get_rental_details()
        elif option == "12":
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
        app.set_logged_in_user(user)

        print_success("User was edited successfully.")
    except Exception as e:
        db_conn.rollback()

        print_error(f"Error in updating user info: {str(e)}")

    wait_on_enter()


def view_film_list():
    clear_screen()
    print_header("Film List")

    print("--- Categories ---")
    category_list_insert = "SELECT * FROM category"
    db_cursor.execute(category_list_insert)
    cat_list = db_cursor.fetchall()
    for category in cat_list:
        print(category)

    selected_category_id = input("Input the category ID: ")
    db_cursor.execute(
        f"SELECT * FROM film JOIN film_category USING(film_id) WHERE category_id={selected_category_id} ORDER BY rate DESC, title")
    films = db_cursor.fetchall()

    for film in films:
        print(film)

    wait_on_enter()


def search_films():
    clear_screen()
    print_header("Search Films")

    print("1. By Actor")
    print("2. By Genre")
    print("3. By Film Name")
    print("4. By Film Language")
    print("5. By Release Year")

    option = read_menu_opt()

    search_query = input("Enter your search query: ")
    if option == "1":
        query = f"SELECT * FROM film JOIN plays USING (film_id) JOIN actor USING (actor_id) WHERE first_name LIKE '%{
            search_query}%' OR last_name LIKE '%{search_query}%'"
    elif option == "2":
        query = f"SELECT * FROM film JOIN film_category USING (film_id) JOIN category USING (category_id) WHERE category_name LIKE '%{
            search_query}%'"
    elif option == "3":
        query = f"SELECT * FROM film WHERE title LIKE '%{search_query}%'"
    elif option == "4":
        query = f"SELECT * FROM film JOIN film_language USING (film_id) JOIN language USING (language_id) WHERE language_name LIKE '%{
            search_query}%'"
    elif option == "5":
        query = f"SELECT * FROM film WHERE YEAR(release_date) = {search_query}"
    else:
        print_error("Invalid option")
        wait_on_enter()
        return

    db_cursor.execute(query)
    films = db_cursor.fetchall()

    for f in films:
        print(f)

    wait_on_enter()


def get_rental_details():
    clear_screen()
    print_header("Rental Details")

    db_cursor.execute("""
              SELECT film_id, title, AVG(rental.rate), COUNT(dvd_id)
              FROM rental JOIN dvd USING (dvd_id) JOIN film USING (film_id)
              GROUP BY film_id""")
    rental_details = db_cursor.fetchall()

    for rental in rental_details:
        print(rental)

    wait_on_enter()

def get_rental_history():
    clear_screen()
    print_header("Rental History")

    logged_in_user_id = app.logged_in_user.user_id
    db_cursor.execute(f"SELECT * FROM rental WHERE customer_id={logged_in_user_id}")
    history = db_cursor.fetchall()

    print(history)

    wait_on_enter()

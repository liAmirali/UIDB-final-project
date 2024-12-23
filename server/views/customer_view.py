import datetime

from tabulate import tabulate

from views.utils import *
from db.db import db_cursor, db_conn
from src.app import app
from models.user import User


def show_customer_screen():
    while True:
        clear_screen()
        print_header("Customer View")

        print(" 1. All Shops")
        print(" 2. View and Edit profile")
        print(" 3. Films by category")
        print(" 4. Search Films")
        print(" 5. Rental Details")
        print(" 6. Rental History")
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
        elif option == "6":
            get_rental_history()
        elif option == "7":
            reserve_film()
        elif option == '8':
            rent_dvd()
        elif option == '9':
            return_dvd()
        elif option == '10':
            show_active_rents()
        elif option == '11':
            show_payment_information()
        elif option == "12":
            break


def get_all_shops():
    clear_screen()
    print_header("Shop List")

    db_cursor.execute(
        "SELECT shop_id, shop_name, first_name, last_name, manager_id, address_id FROM shop JOIN user ON shop.manager_id=user.user_id JOIN address USING address_id")
    all_shops = db_cursor.fetchall()

    headers = ["Shop ID", "Shop Name", "Manager First Name",
               "Manager Last Name", "Manager ID", "Address ID"]
    print(tabulate(all_shops, headers=headers, tablefmt="pretty"))

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
        headers = ["User ID", "First Name", "Last Name",
                   "Username", "Password", "Email", "Address ID", "Role"]
        print(tabulate([foundUser], headers=headers, tablefmt="pretty"))

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

    headers = ["Film ID", "Title", "Description", "Release Date",
               "Rate", "Rent Cost per Day", "Penalty Cost per Day"]
    print(tabulate(films, headers=headers, tablefmt="pretty"))

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

    headers = ["Film ID", "Title", "Description", "Release Date",
               "Rate", "Rent Cost per Day", "Penalty Cost per Day"]
    print(tabulate(films, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def get_rental_details():
    clear_screen()
    print_header("Rental Details")

    db_cursor.execute("""
              SELECT film_id, title, AVG(rental.rate), COUNT(dvd_id)
              FROM rental JOIN dvd USING (dvd_id) JOIN film USING (film_id)
              GROUP BY film_id""")
    rental_details = db_cursor.fetchall()

    headers = ["Film ID", "Title", "Average Rate", "Number of DVDs"]
    print(tabulate(rental_details, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def get_rental_history():
    clear_screen()
    print_header("Rental History")

    logged_in_user_id = app.logged_in_user.user_id
    db_cursor.execute(
        f"SELECT * FROM rental WHERE customer_id={logged_in_user_id}")
    history = db_cursor.fetchall()

    headers = ["Rental ID", "Customer ID", "DVD ID", "Rental Date",
               "Due Date", "Return Date", "Rate", "Status", "Last Update"]
    print(tabulate(history, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def reserve_film():
    clear_screen()
    print_header("Reserve a Film")

    logged_in_user_id = app.logged_in_user.user_id

    selected_film_id = input("Please enter the film ID you want to reserve: ")
    db_cursor.execute(
        f"""SELECT dvd_id, shop_name
        FROM dvd
            JOIN film USING (film_id)
            JOIN shop USING (shop_id)
        WHERE film_id={selected_film_id}
        EXCEPT
        SELECT dvd_id, shop_name
        FROM reserve
            JOIN dvd USING (dvd_id)
            JOIN shop USING (shop_id)
        WHERE film_id={selected_film_id} AND expired=0
        """)

    result = db_cursor.fetchall()
    if result is None or len(result) == 0:
        print_error("No DVDs found for this film.")
    else:
        headers = ["DVD ID", "Shop Name"]
        print(tabulate(result, headers=headers, tablefmt="pretty"))

        selected_dvd_id = input("Select a DVD ID: ")
        found = False
        for res in result:
            if str(res[0]) == selected_dvd_id:
                found = True
                break
        if not found:
            print_error("Your selected DVD is not available.")
        else:
            try:
                db_cursor.execute("INSERT INTO reserve (customer_id, dvd_id) VALUES (%s, %s)", (
                    logged_in_user_id, int(selected_dvd_id)))

                db_conn.commit()
                print_success("DVD was reserved successfully.")
            except Exception as e:
                db_conn.rollback()
                print_error(f"Error in reserving: {str(e)}")

    wait_on_enter()


def rent_dvd():
    clear_screen()
    print_header("Rent a Film")

    logged_in_user_id = app.logged_in_user.user_id

    selected_film_id = input("Please enter the film ID you want to rent: ")
    db_cursor.execute(
        f"""SELECT dvd_id, shop_name
        FROM dvd
            JOIN film USING (film_id)
            JOIN shop USING (shop_id)
        WHERE film_id={selected_film_id}
        EXCEPT
        SELECT dvd_id, shop_name
        FROM reserve
            JOIN dvd USING (dvd_id)
            JOIN shop USING (shop_id)
        WHERE film_id={selected_film_id} AND expired=0
        EXCEPT
        SELECT dvd_id, shop_name
        FROM rental
            JOIN dvd USING (dvd_id)
            JOIN shop USING (shop_id)
        WHERE status='accepted' AND return_date IS NULL
        """)

    result = db_cursor.fetchall()
    if result is None or len(result) == 0:
        print_error("No DVDs found for this film.")
    else:
        headers = ["DVD ID", "Shop Name"]
        print(tabulate(result, headers=headers, tablefmt="pretty"))

        selected_dvd_id = input("\nSelect a DVD ID: ")
        found = False
        for res in result:
            if str(res[0]) == selected_dvd_id:
                found = True
                break
        if not found:
            print_error("Your selected DVD is not available.")
        else:
            try:
                db_cursor.execute("INSERT INTO rental (customer_id, dvd_id) VALUES (%s, %s)", (
                    logged_in_user_id, int(selected_dvd_id)))

                db_conn.commit()
                print_success("DVD was rented successfully.")
            except Exception as e:
                db_conn.rollback()
                print_error(f"Error in renting: {str(e)}")

    wait_on_enter()


def return_dvd():
    clear_screen()
    print_header("Return a DVD")

    logged_in_user_id = app.logged_in_user.user_id
    db_cursor.execute(f"""SELECT
                      rental_id,
                      dvd_id, shop_name,
                      rental_date, due_date, TIMESTAMPDIFF(DAY, rental_date, due_date) as remaining_time,
                      rent_cost_per_day, penalty_cost_per_day
                      FROM rental
                        JOIN dvd USING (dvd_id)
                        JOIN shop USING (shop_id)
                        JOIN film USING (film_id)
                      WHERE customer_id={logged_in_user_id} AND return_date is NULL AND status='accepted'
    """)
    active_rents = db_cursor.fetchall()

    if active_rents is None or len(active_rents) == 0:
        print_error("No active rent!")
    else:
        headers = ["Rental ID", "DVD ID", "Shop Name", "Rented At",
                   "Due Date", "Remaining Time", "Cost per day", "Penalty per day"]
        print(tabulate(active_rents, headers=headers, tablefmt="pretty"))

        selected_rental_id = input(
            "\nPlease enter the Rental ID you want to return: ")
        found = False
        for res in active_rents:
            if str(res[0]) == selected_rental_id:
                found = True
                break

        if not found:
            print_error("Your selected DVD is not available.")
        else:
            user_rate = input("Input your rate in range [0-5]:")

            try:
                rental_id = res[0]
                rental_date = res[3]
                due_date = res[4]

                print("rental_date", rental_date)
                print("due_date", due_date)
                rental_duration = (due_date - rental_date).days
                rent_cost_per_day = res[6]
                penalty_cost_per_day = res[7]
                days_after_due_date = max(
                    (datetime.datetime.now() - due_date).days, 0)
                return_cost = rental_duration * rent_cost_per_day + \
                    days_after_due_date * penalty_cost_per_day

                print(f"The cost is ${return_cost}")
                payment_confirmed = input("Pay and Return? (Y/N): ")
                if payment_confirmed == "Y" or payment_confirmed == "y":
                    db_cursor.execute(f"""UPDATE rental
                                    SET return_date=NOW(),
                                    rate={user_rate}
                                    WHERE rental_id={selected_rental_id} """)

                    db_cursor.execute(
                        "INSERT INTO payment (rental_id, amount) VALUES (%s, %s)", (rental_id, return_cost))

                db_conn.commit()
                print_success("DVD was returned successfully.")
            except Exception as e:
                db_conn.rollback()
                print_error(f"Error in renting: {str(e)}")

    wait_on_enter()


def show_active_rents():
    clear_screen()
    print_header("Active Rents")

    logged_in_user_id = app.logged_in_user.user_id
    db_cursor.execute(f"""SELECT
                      rental_id,
                      dvd_id, shop_name,
                      rental_date, due_date, TIMESTAMPDIFF(DAY, rental_date, due_date) as remaining_time,
                      rent_cost_per_day, penalty_cost_per_day
                      FROM rental
                        JOIN dvd USING (dvd_id)
                        JOIN shop USING (shop_id)
                        JOIN film USING (film_id)
                      WHERE customer_id={logged_in_user_id} AND return_date is NULL AND status='accepted'
    """)
    active_rents = db_cursor.fetchall()

    if active_rents is None or len(active_rents) == 0:
        print_error("No active rents!")
    else:
        headers = ["Rental ID", "DVD ID", "Shop Name", "Rented At",
                   "Due Date", "Remaining Time", "Cost per day", "Penalty per day"]
        print(tabulate(active_rents, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def show_payment_information():
    clear_screen()
    print_header("Payment Information")

    customer_id = app.logged_in_user.user_id

    db_cursor.execute(
        f"SELECT * FROM payment JOIN rental USING (rental_id) WHERE customer_id={customer_id}")
    result = db_cursor.fetchall()

    headers = ["Rental ID", "Payment ID", "Payment Date", "Customer ID",
               "DVD ID", "Rental Date", "Due Date", "Return Date" "Amount",
               "Status", "Rate", "Last Update"]
    print(tabulate(result, headers=headers, tablefmt="pretty"))

    wait_on_enter()

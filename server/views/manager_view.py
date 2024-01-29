from models.user import User
from views.utils import *
from src.app import app
from db.db import db_conn, db_cursor
from utils.input import get_datetime_input

from tabulate import tabulate


def show_manager_screen():
    while True:
        clear_screen()
        print_header("Manager Page")

        print(" 1. Customer List")
        print(" 2. Film Rental Details")
        print(" 3. Active Rentals")
        print(" 4. Rent Requests")
        print(" 5. Reserve Requests")
        print(" 6. View Shop Info")
        print(" 7. Edit Shop Info")
        print(" 8. All Films")
        print(" 9. All Films by Category")
        print("10. Search on Films")
        print("11. Payment Details")
        print("12. Best-Sellers")
        print("13. Exit")

        option = read_menu_opt()

        if option == "1":
            show_customer_list()
        elif option == "2":
            show_rental_details()
        elif option == "3":
            show_active_rentals()
        elif option == "4":
            show_rent_requests()
        elif option == "5":
            show_reserve_requests()
        elif option == "6":
            show_shop_info()
        elif option == "7":
            edit_shop_info()
        elif option == "8":
            view_all_films()
        elif option == "9":
            show_films_by_cat()
        elif option == "10":
            search_films()
        elif option == "11":
            show_payment_details()
        elif option == "12":
            show_best_seller()
        elif option == "13":
            break


def show_customer_list():

    clear_screen()
    print_header("Customer List")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""
    SELECT s.shop_name, u.user_id, u.first_name, u.last_name, u.username, u.email
    FROM user u
    JOIN rental r ON u.user_id = r.customer_id
    JOIN dvd d ON r.dvd_id = d.dvd_id
    JOIN shop s ON d.shop_id = s.shop_id
    WHERE s.manager_id = {manager_id}
    ORDER BY s.shop_name"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Shop Name", "User ID", "First Name",
               "Last Name", "Username", "Email"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def show_rental_details():

    clear_screen()
    print_header("Rental Details")

    film_id = input("Enter Film ID: ")

    sql_query = f"""SELECT
    f.title AS film_title,
    COUNT(r.rental_id) AS number_of_rents,
    AVG(r.rate) AS average_score,
    COUNT(d.dvd_id) AS number_of_dvds,
    SUM(CASE WHEN r.return_date > r.due_date THEN 1 ELSE 0 END) AS number_of_delays
    FROM film f
    LEFT JOIN dvd d ON f.film_id = d.film_id
    LEFT JOIN rental r ON d.dvd_id = r.dvd_id
    WHERE
    f.film_id = {film_id}"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Film Title", "Number of Rents",
               "Average Score", "Number of DVDs", "Number of Delays"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def show_active_rentals():

    clear_screen()
    print_header("Active Rental")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT
    r.rental_id,
    r.customer_id,
    r.dvd_id,
    r.rental_date,
    r.due_date
    FROM
        rental r
    JOIN
        dvd d ON r.dvd_id = d.dvd_id
    JOIN
        shop s ON d.shop_id = s.shop_id
    WHERE
    s.manager_id = {manager_id}
    AND r.status = "accepted" AND r.return_date IS NULL"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Rental ID", "Customer ID", "DVD ID", "Rental Date", "Due Date"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def show_rent_requests():

    clear_screen()
    print_header("Rent Requests")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT
    r.rental_id,
    r.customer_id,
    r.dvd_id,
    r.rental_date,
    r.due_date
    FROM
        rental r
    JOIN
        dvd d ON r.dvd_id = d.dvd_id
    JOIN
        shop s ON d.shop_id = s.shop_id
    WHERE
        s.manager_id = {manager_id}
        AND r.status = "checking"
    """

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Rental ID", "Customer ID", "DVD ID", "Rental Date", "Due Date"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    rent_id = input("\nEnter rent ID to reject/accept (Enter \'0\' to exit): ")
    if rent_id == "0":
        return
    else:
        found = False
        for rental in foundlist:
            if str(rental[0]) == rent_id:
                found = True
                break
        if not found:
            print_error("Rental was not found.")
            wait_on_enter()
            return

        rejectAccept = input("Enter \"R\" to Reject or \"A\" to Accept: ")

        if rejectAccept == "R":
            try:
                db_cursor.execute(
                    f"UPDATE rental SET status='rejected' WHERE rental_id={rent_id}")
                print_success("Rental was rejected successfully.")
            except Exception as e:
                db_conn.rollback()
                print_error(f"Error rejecting rental: {e}")

        elif rejectAccept == "A":
            try:
                rental_datetime = get_datetime_input("Enter rental datetime")
                due_datetime = get_datetime_input("Enter due datetime")

                db_cursor.execute(f"""UPDATE rental
                                  SET status='accepted', rental_date='{rental_datetime}', due_date='{due_datetime}'
                                  WHERE rental_id={rent_id}""")
                db_conn.commit()

                print_success("Rental was accepted successfully.")
            except Exception as e:
                db_conn.rollback()
                print_error(f"Error accepting rental: {e}")
        else:
            print("Exiting...")

    wait_on_enter()


def show_reserve_requests():

    clear_screen()
    print_header("Reserve Requests")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT
    r.reserve_id,
    r.customer_id,
    r.dvd_id,
    r.created_at
    FROM
        reserve r
    JOIN
        dvd d ON r.dvd_id = d.dvd_id
    JOIN
        shop s ON d.shop_id = s.shop_id
    WHERE
        s.manager_id = {manager_id}
        AND r.expired = 0"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Reserve ID", "Customer ID", "DVD ID", "Created At"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    reserve_id = input(
        "\nEnter reserve ID to reject/accept (Enter '0' to exit): ")
    if reserve_id == "0":
        return
    else:
        found = False
        for reserve in foundlist:
            if str(reserve[0]) == reserve_id:
                found = True
                break
        if not found:
            print_error("Reservation was not found.")
            wait_on_enter()
            return

        rejectAccept = input("Enter 'R' to Reject or 'A' to Accept: ")

        if rejectAccept == "R":
            try:
                db_cursor.execute(
                    f"UPDATE reserve SET accepted = 0 WHERE reserve_id={reserve_id}")
                print_success("Reservation was rejected successfully.")
            except Exception as e:
                db_conn.rollback()
                print_error(f"Error rejecting reservation: {e}")

        elif rejectAccept == "A":
            try:
                db_cursor.execute(f"""UPDATE reserve
                                  SET accepted = 1, check_date = NOW()
                                  WHERE reserve_id={reserve_id}""")
                db_conn.commit()

                print_success("Reservation was accepted successfully.")
            except Exception as e:
                db_conn.rollback()
                print_error(f"Error accepting reservation: {e}")
        else:
            print("Exiting...")

    wait_on_enter()


def show_shop_info():

    clear_screen()
    print_header("Shop info")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT
    s.shop_id,
    s.shop_name,
    u.user_id AS manager_id,
    u.first_name AS manager_first_name,
    u.last_name AS manager_last_name,
    a.address,
    a.address2,
    a.district,
    a.postal_code,
    a.phone,
    a.location,
    a.city,
    a.country
    FROM
        shop s
    JOIN
        user u ON s.manager_id = u.user_id
    JOIN
        address a ON s.address_id = a.address_id
    WHERE
    s.manager_id = {manager_id}"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Shop ID", "Shop Name", "Manager ID", "Manager First Name", "Manager Last Name",
               "Address", "Address2", "District", "Postal Code", "Phone", "Location", "City", "Country"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def edit_shop_info():
    clear_screen()
    print_header("Edit Shop Info")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT shop_id, shop_name, address_id FROM shop WHERE manager_id = {
        manager_id}"""
    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    print("--- Your shops ---")
    for shop in foundlist:
        print(shop)

    shop_id = input("Enter the shop_id: ")

    for shop in foundlist:
        if shop[0] == shop_id:
            address_id = shop[2]

    print("* Hit enter to keep the old value *")

    print("\n --- Shop Information ---")

    shop_name = input("Shop_name: ")

    print("\n --- Address ---")

    address = input("Address: ")
    address2 = input("Address 2: ")
    district = input("District: ")
    postal_code = input("Postal Code: ")
    phone = input("Phone: ")
    location = input("Location: ")
    city = input("City: ")
    country = input("Country: ")

    update_shop_query = f"""UPDATE user
    SET
        shop_name = {'"' + shop_name + '"' if shop_name != "" else 'shop_name'}
    WHERE
        shop_id = {shop_id}"""

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
        address_id = {address_id}"""

    print("update_address_query:", update_address_query)

    try:
        db_cursor.execute(update_shop_query)
        db_cursor.execute(update_address_query)

        db_conn.commit()

        print_success("Shop was edited successfully.")
    except Exception as e:
        db_conn.rollback()

        print_error(f"Error in updating shop info: {str(e)}")

    wait_on_enter()


def view_all_films():

    clear_screen()
    print_header("All Films")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT
    f.title AS film_title,
    f.description,
    f.release_date,
    f.rate,
    f.rent_cost_per_day,
    f.penalty_cost_per_day
    FROM
        film f
    JOIN
        dvd d ON f.film_id = d.film_id
    JOIN
        shop s ON d.shop_id = s.shop_id
    WHERE
        s.manager_id = {manager_id}
    ORDER BY
        f.rate DESC"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Film Title", "Description", "Release Date",
               "Rate", "Rent Cost Per Day", "Penalty Cost Per Day"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def show_payment_details():
    clear_screen()
    print_header("Payment Details")

    print("1. Show all payments")
    print("2. Show payments of specific customer")
    print("3. Show payments of specific film")

    manager_id = app.logged_in_user.user_id
    option = read_menu_opt()

    if option == "1":

        sql_query = f"""SELECT
        p.payment_id,
        p.rental_id,
        f.title,
        p.payment_date,
        p.amount,
        r.customer_id,
        r.dvd_id,
        r.return_date,
        s.shop_name
        FROM
            payment p
        JOIN
            rental r ON p.rental_id = r.rental_id
        JOIN
            dvd d ON r.dvd_id = d.dvd_id
        JOIN
            shop s ON d.shop_id = s.shop_id
        JOIN
            film f ON d.film_id = f.film_id
        WHERE
        s.manager_id = {manager_id}"""

    elif option == "2":

        customer_id = input("Enter customer ID:")  # 2

        sql_query = f"""SELECT
        p.payment_id,
        p.rental_id,
        f.title,
        p.payment_date,
        p.amount,
        r.customer_id,
        r.dvd_id,
        r.return_date,
        s.shop_name
        FROM
            payment p
        JOIN
            rental r ON p.rental_id = r.rental_id
        JOIN
            dvd d ON r.dvd_id = d.dvd_id
        JOIN
            shop s ON d.shop_id = s.shop_id
        JOIN
            film f ON d.film_id = f.film_id
        WHERE
            s.manager_id = {manager_id} AND r.customer_id = {customer_id}"""

    elif option == "3":
        film_id = input("Enter film ID:")  # 10

        sql_query = f"""SELECT
        p.payment_id,
        p.rental_id,
        f.title,
        f.film_id,
        p.payment_date,
        p.amount,
        r.customer_id,
        r.dvd_id,
        r.return_date,
        s.shop_name
        FROM
            payment p
        JOIN
            rental r ON p.rental_id = r.rental_id
        JOIN
            dvd d ON r.dvd_id = d.dvd_id
        JOIN
            shop s ON d.shop_id = s.shop_id
        JOIN
            film f ON d.film_id = f.film_id
        WHERE
            s.manager_id = {manager_id} AND f.film_id = {film_id}"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    headers = ["Payment ID", "Rental ID", "Film Title", "Payment Date",
               "Amount", "Customer ID", "DVD ID", "Return Date", "Shop Name"]
    print(tabulate(foundlist, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def show_films_by_cat():
    clear_screen()
    print_header("Films By Category")

    manager_id = app.logged_in_user.user_id
    sql_query = f"""SELECT s.shop_id, s.shop_name, GROUP_CONCAT(DISTINCT c.category_name) AS categories
                        FROM shop s
                        JOIN dvd d ON s.shop_id = d.shop_id
                        JOIN film f ON d.film_id = f.film_id
                        JOIN film_category fc ON f.film_id = fc.film_id
                        JOIN category c ON fc.category_id = c.category_id
                        WHERE s.manager_id = {manager_id}
                        GROUP BY s.shop_id, s.shop_name"""

    db_cursor.execute(sql_query)
    shop_categories = db_cursor.fetchall()

    headers = ["Shop ID", "Shop Name", "Categories"]
    print(tabulate(shop_categories, headers=headers, tablefmt="pretty"))

    print("\n --- Select Shop and Category ---")
    shop_id = input("Enter shop_id: ")
    category_name = input("Enter category name: ")

    sql_query = f"""SELECT f.film_id, f.title, f.description, f.release_date
                    FROM film f
                    JOIN film_category fc ON f.film_id = fc.film_id
                    JOIN category c ON fc.category_id = c.category_id
                    JOIN dvd d ON f.film_id = d.film_id
                    WHERE c.category_name = '{category_name}' AND d.shop_id = {shop_id}"""

    db_cursor.execute(sql_query)
    result = db_cursor.fetchall()

    headers = ["Film ID", "Title", "Description", "Release Date"]
    print(tabulate(result, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def show_best_seller():
    clear_screen()
    print_header("Films By Category")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT shop_id, shop_name FROM shop WHERE manager_id = {
        manager_id}"""
    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    print("--- Your shops ---")
    for shop in foundlist:
        print(shop)

    shop_id = input("Enter the shop_id: ")

    print("1- BestSeller Film")
    print("2- BestSeller Category")
    print("3- BestSeller Actor")

    opt = input("Enter command number: ")

    if opt == "1":
        sql_query = f"""SELECT f.film_id, f.title, COUNT(r.rental_id) as rental_count
                        FROM film f
                        JOIN dvd d ON f.film_id = d.film_id
                        JOIN rental r ON d.dvd_id = r.dvd_id
                        JOIN shop s ON d.shop_id = s.shop_id
                        WHERE s.shop_id = {shop_id}
                        GROUP BY f.film_id, f.title
                        ORDER BY rental_count DESC
                        LIMIT 1"""
    elif opt == "2":
        sql_query = f"""SELECT c.category_name, COUNT(r.rental_id) as rental_count
                        FROM category c
                        JOIN film_category fc ON c.category_id = fc.category_id
                        JOIN film f ON fc.film_id = f.film_id
                        JOIN dvd d ON f.film_id = d.film_id
                        JOIN rental r ON d.dvd_id = r.dvd_id
                        JOIN shop s ON d.shop_id = s.shop_id
                        WHERE s.shop_id = {shop_id}
                        GROUP BY c.category_id, c.category_name
                        ORDER BY rental_count DESC
                        LIMIT 1"""
    elif opt == "3":
        sql_query = f"""SELECT a.actor_id, a.first_name, a.last_name, COUNT(r.rental_id) as rental_count
                        FROM actor a
                        JOIN plays p ON a.actor_id = p.actor_id
                        JOIN film f ON p.film_id = f.film_id
                        JOIN dvd d ON f.film_id = d.film_id
                        JOIN rental r ON d.dvd_id = r.dvd_id
                        JOIN shop s ON d.shop_id = s.shop_id
                        WHERE s.shop_id = {shop_id}
                        GROUP BY a.actor_id, a.first_name, a.last_name
                        ORDER BY rental_count DESC
                        LIMIT 1"""

    db_cursor.execute(sql_query)
    result = db_cursor.fetchall()

    headers = ["ID", "Name", "Rental Count"]
    print(tabulate(result, headers=headers, tablefmt="pretty"))

    wait_on_enter()


def search_films():
    clear_screen()
    print_header("Search Films")

    manager_id = app.logged_in_user.user_id

    sql_query = f"""SELECT shop_id, shop_name FROM shop WHERE manager_id = {
        manager_id}"""
    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    print("--- Your shops ---")
    for shop in foundlist:
        print(shop)

    shop_id = input("Enter the shop_id: ")

    print("1. By Actor")
    print("2. By Genre")
    print("3. By Film Name")
    print("4. By Film Language")
    print("5. By Release Year")

    option = read_menu_opt()

    search_query = input("Enter your search query: ")
    if option == "1":
        query = f"SELECT * FROM film JOIN dvd d USING (film_id) JOIN plays USING (film_id) JOIN actor USING (actor_id) WHERE d.shop_id = {
            shop_id} AND first_name LIKE '%{search_query}%' OR last_name LIKE '%{search_query}%'"
    elif option == "2":
        query = f"SELECT * FROM film JOIN dvd d USING (film_id) JOIN film_category USING (film_id) JOIN category USING (category_id) WHERE d.shop_id = {
            shop_id} AND category_name LIKE '%{search_query}%'"
    elif option == "3":
        query = f"SELECT * FROM film JOIN dvd d USING (film_id) WHERE d.shop_id = {
            shop_id} AND title LIKE '%{search_query}%'"
    elif option == "4":
        query = f"SELECT * FROM film JOIN dvd d USING (film_id) JOIN film_language USING (film_id) JOIN language USING (language_id) WHERE d.shop_id = {
            shop_id} AND language_name LIKE '%{search_query}%'"
    elif option == "5":
        query = f"SELECT * FROM film JOIN dvd d USING (film_id) WHERE d.shop_id = {
            shop_id} AND YEAR(release_date) = {search_query}"
    else:
        print_error("Invalid option")
        wait_on_enter()
        return

    db_cursor.execute(query)
    films = db_cursor.fetchall()

    headers = ["Film ID", "Title", "Description", "Release Date"]
    print(tabulate(films, headers=headers, tablefmt="pretty"))

    wait_on_enter()

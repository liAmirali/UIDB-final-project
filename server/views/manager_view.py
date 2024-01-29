from views.utils import *
from src.app import app
from db.db import db_conn, db_cursor


def show_manager_screen():
    while True:
        clear_screen()
        print_header("Manager Page")

        print(" 1. Show customer list")
        print(" 2. Show rental detail of a film")
        print(" 3. Show active rentals")
        print(" 4. Show rent requests")
        print(" 5. Show reserve requests")
        print(" 6. Show shop info")
        print(" 7. Edit shop info")
        print(" 8. View all films")
        print(" 9. View all films by category")
        print("10. Search on films")
        print("11. Payment details")
        print("12. BestSeller films")

        option = read_menu_opt()

        if option == "1":
            show_customer_list()
        elif option == "2":
            show_rental_detail()
        elif option == "3":
            show_active_rentals()
        elif option == "4":
            show_rent_requests()
        elif option == "5":
            show_reserve_requests()
        elif option == "6":
            show_shop_info()
        elif option == "7":
            pass
        elif option == "8":
            view_all_films()
        elif option == "9":
            pass
        elif option == "10":
            pass
        elif option == "11":
            show_payment_details()
        elif option == "12":
            pass
        elif option == "13":
            break


def show_customer_list():

    clear_screen()
    print_header("Customer List")

    manager_id = 6
    # manager_id = app.logged_in_user.user_id
    sql_query = f"""
    SELECT s.shop_name, u.user_id, u.first_name, u.last_name, u.username, u.email
    FROM user u
    JOIN rental r ON u.user_id = r.customer_id
    JOIN dvd d ON r.dvd_id = d.dvd_id
    JOIN shop s ON d.shop_id = s.shop_id
    WHERE s.manager_id = {manager_id}"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    print(foundlist)
    wait_on_enter()


def show_rental_detail():

    clear_screen()
    print_header("Rental Detail")

    film_id = input("Enter film_id:")

    sql_query = f"""SELECT
    f.title AS film_title,
    COUNT(r.rental_id) AS number_of_rents,
    AVG(f.rate) AS average_score,
    COUNT(d.dvd_id) AS number_of_dvds,
    SUM(CASE WHEN r.return_date > r.due_date THEN 1 ELSE 0 END) AS number_of_delays
    FROM film f
    LEFT JOIN dvd d ON f.film_id = d.film_id
    LEFT JOIN rental r ON d.dvd_id = r.dvd_id
    WHERE
    f.film_id = {film_id}"""

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    print(foundlist)
    wait_on_enter()


def show_active_rentals():

    clear_screen()
    print_header("Active Rental")

    manager_id = 6
    # manager_id = app.logged_in_user.user_id

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

    print(foundlist)
    wait_on_enter()


def show_rent_requests():

    clear_screen()
    print_header("Rent Requests")

    manager_id = 6
    # manager_id = app.logged_in_user.user_id

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

    print(foundlist)
    wait_on_enter()


def show_reserve_requests():

    clear_screen()
    print_header("Reserve Requests")

    manager_id = 6
    # manager_id = app.logged_in_user.user_id

    sql_query = f""" SELECT
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
        AND r.accepted is NULL """

    db_cursor.execute(sql_query)
    foundlist = db_cursor.fetchall()

    print(foundlist)
    wait_on_enter()


def show_shop_info():

    clear_screen()
    print_header("Shop info")

    manager_id = 6
    # manager_id = app.logged_in_user.user_id

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

    print(foundlist)
    wait_on_enter()


def view_all_films():

    clear_screen()
    print_header("All Film")

    manager_id = 6
    # manager_id = app.logged_in_user.user_id

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

    print(foundlist)
    wait_on_enter()


def show_payment_details():
    clear_screen()
    print_header("Payment Details")

    print("1. Show all payments")
    print("2. Show payments of specific customer")
    print("3. Show payments of specific film")

    manager_id = 6
    # manager_id = app.logged_in_user.user_id
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

    print(foundlist)
    wait_on_enter()

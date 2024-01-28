from views.utils import *
from src.app import app
from db.db import db_conn, db_cursor


def show_manager_screen():
    while True:
        clear_screen()
        print_header("Manager Page")

        print("1. Show customer list")
        print("2. Show rental detail of a film")
        print("3. Show active rentals")
        print("4. Show rent requests")
        print("5. show reserve requests")
        print("6. show shop info")
        print("7. Edit shop info")
        print("8. View all films")
        print("9. View all films by category")
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
            pass
        elif option == "6":
            pass
        elif option == "7":
            pass
        elif option == "8":
            pass
        elif option == "9":
            pass
        elif option == "10":
            pass
        elif option == "11":
            pass
        elif option == "12":
            pass
        elif option == "13":
            break


def show_customer_list():

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
    

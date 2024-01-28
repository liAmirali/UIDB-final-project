from views.utils import clear_screen, wait_on_enter, print_header, read_menu_opt;

def show_login_screen():
    clear_screen()
    print_header("Login Page")

    print("1. Login as a Manager")
    print("2. Login as a Customer")
    print("3. Exit")

    option = read_menu_opt()
    if (option == "1"):
        get_login_credentials("manager")
    elif (option == "2"):
        get_login_credentials("customer")
    elif (option == "3"):
        print("Good bye!")
        return

def get_login_credentials(role):
    print("Username: ")
    print("Password: ")

    if role == "manager":
        pass
    elif role == "customer":
        pass

    # TODO: Query username and password
    # TODO: Set the app user object


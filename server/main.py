from views.auth_view import show_login_screen
from views.manager_view import show_manager_screen
from db.db import db_cursor

if __name__ == '__main__':
    show_manager_screen()

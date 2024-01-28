class User:
    def __init__(self, user_id, username, role, first_name, last_name, email):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

class App:
    def __init__(self):
        self.logged_in_user = None

    def set_logged_in_user(self, user: User):
        self.logged_in_user = user

app = App()

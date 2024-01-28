from models.user import User
class App:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logged_in_user = None
        return cls._instance

    def set_logged_in_user(self, user: User):
        self.logged_in_user = user

app = App()

class User:
    # def __init__(self, user_id, username, role, first_name, last_name, email):
    #     self.user_id = user_id
    #     self.username = username
    #     self.role = role
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email

    def __init__(self, db_user):
        self.user_id = db_user[0]
        self.first_name = db_user[1]
        self.last_name = db_user[2]
        self.username = db_user[3]
        self.email = db_user[5]
        self.address_id = db_user[6]
        self.role = db_user[7]

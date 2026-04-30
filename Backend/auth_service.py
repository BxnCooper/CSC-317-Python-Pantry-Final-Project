from Backend.database import Database

# this class handles the log in and register functions
class AuthService():
    def __init__(self):
        self.db = Database()
        
    # logs in the user
    def login(self, username, password):
        ok = self.db.check_user(username, password)
        if ok:                                  # checks the database to see if the user's password is correct (or account exists)
            return True, {"username": username}
        return False, "Invalid credentials"

    # registers the user into the database 
    def register(self, username, password):
        ok = self.db.add_user(username, password)
        if ok:                                  # checks the database to see if the user was successfully added
            return True, {"username": username}
        return False, "User exists"

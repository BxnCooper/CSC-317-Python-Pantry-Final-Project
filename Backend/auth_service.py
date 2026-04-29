from Backend.database import Database


class AuthService():
    def __init__(self):
        self.db = Database()
        
    def login(self,username, password):
        ok = self.db.check_user(username, password)
        if ok:
            return True, {"username": username}
        return False, "Invalid credentials"


    def register(self, username, password):
        ok = self.db.add_user(username, password)
        if ok:
            return True, {"username": username}
        return False, "User exists"

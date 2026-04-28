from backend.database import add_user, check_user


def login(username, password):
    ok = check_user(username, password)
    if ok:
        return True, {"username": username}
    return False, "Invalid credentials"


def register(username, password):
    ok = add_user(username, password)
    if ok:
        return True, {"username": username}
    return False, "User exists"

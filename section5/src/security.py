import logging, sys
from user import User

def authenticate(username, password):
    ##print("USER: %s, PWD: %s" % (username, password), file=sys.stderr)
    user = User.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    """
    Extracts from JWT (payload) the user_id and
    mamps it to a user.
    """
    user_id = payload["identity"]
    return User.find_by_id(user_id)

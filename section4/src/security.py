import logging, sys
from user import User
users = [
    User(1, "bob", "asdf"),
    User(2, "john", "asdf"),
    User(3, "sam", "asdf"),]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    ##print("USER: %s, PWD: %s" % (username, password), file=sys.stderr)
    user = username_mapping.get(username)
    if user and user.password == password:
        return user

def identity(payload):
    """
    Extracts from JWT (payload) the user_id and
    mamps it to a user.
    """
    user_id = payload["identity"]
    return userid_mapping.get(user_id)

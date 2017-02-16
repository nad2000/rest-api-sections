users = [dict(id=1, username="bob", password="asdf")]

username_mappig = {u["username"]: user for user in users}
userid_mapping = {u["id"]: user for user in users}

def authenticate(username, password):
    user = username_mappig.get(username)
    if user and user["password"] == password:
        return user

def identity(payload):
    user_id = payload["identity"]
    return userid_mapping.get(user_id)

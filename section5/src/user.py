import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __getitem__(self, key):
        if key == "id":
            return self.id
        return None

    @classmethod
    def find_user(cls, username=None, _id=None):
        connnection = sqlite3.connect("data.db")
        cursor = connnection.cursor()
        if username:
            result = cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        else:
            result = cursor.execute("SELECT * FROM users WHERE id=?", (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connnection.close()
        return user

    @classmethod
    def find_by_username(cls, username):
        return cls.find_user(username=username)

    @classmethod
    def find_by_id(cls, _id):
        return cls.find_user(_id=_id)

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
        conn = sqlite3.connect("data.db")
        if username:
            result = conn.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
        else:
            result = conn.execute("SELECT id, username, password FROM users WHERE id=?", (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.commit()
        conn.close()
        return user

    @classmethod
    def find_by_username(cls, username):
        return cls.find_user(username=username)

    @classmethod
    def find_by_id(cls, _id):
        return cls.find_user(_id=_id)

    @classmethod
    def insert_user(cls, username, password):
        conn = sqlite3.connect("data.db")

        conn.execute("INSERT INTO users (username, password) VALUES(?, ?)",
                (username, password,))

        conn.commit()
        conn.close()
        

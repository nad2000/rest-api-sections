import sqlite3
from flask_restful import Resource, reqparse

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

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",
            type=str,
            required=True,
            help="This field cannot be left blank! It should be string."
    )
    parser.add_argument("password",
            type=str,
            required=True,
            help="This field cannot be left blank! It should be string."
    )

    def post(self):
        data = self.parser.parse_args()
        username, password = data["username"], data["password"]

        if User.find_user(username):
            return {"message": "User '%s' already exists." % username}, 400

        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username, password) VALUES(?, ?)",
                (username, password,))

        conn.commit()
        conn.close()

        return {"message": "User '%s' created successfully." % username}, 201


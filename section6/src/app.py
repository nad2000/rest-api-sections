from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import sqlite3

from security import authenticate, identity
from resources.user import UserRegister

from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = "%*R)(FJ)W$J)$JR)J)WU$"

@app.route("/cleandb")
def cleandb():
    conn = sqlite3.connect("data.db")
    conn.executescript("""
        DELETE FROM users;
        DELETE FROM items;
        """)
    conn.commit()
    conn.close()
    return "OK"

api = Api(app)

jwt = JWT(app, authenticate, identity) ## creates a new endpoint /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run(port=5000, debug=True)


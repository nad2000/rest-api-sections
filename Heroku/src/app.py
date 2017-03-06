import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
import sqlite3

from pyinfo import info

from security import authenticate, identity
from resources.user import UserRegister

from resources.item import ItemResource, ItemListResource
from resources.store import StoreResource, StoreListResource

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.secret_key = "%*R)(FJ)W$J)$JR)J)WU$"

api = Api(app)

jwt = JWT(app, authenticate, identity) ## creates a new endpoint /auth

api.add_resource(ItemResource, "/item/<string:name>")
api.add_resource(ItemListResource, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreResource, "/store/<string:name>")
api.add_resource(StoreListResource, "/stores")

@app.route("/cleandb")
def cleandb():
    conn = sqlite3.connect("data.db")
    conn.executescript("""
        DELETE FROM users;
        DELETE FROM items;
        DELETE FROM stores;
        """)
    conn.commit()
    conn.close()
    return "OK"

@app.route('/pyinfo')
def pyinfo():
    return render_template('pyinfo.html', **info)

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)


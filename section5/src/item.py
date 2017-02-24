import sqlite3
from flask_restful import Resource, reqparse
from security import authenticate, identity
from flask_jwt import jwt_required

def find_item(name):
    return next(filter(lambda i: i.get("name") == name, items), None)

def dict_factory(cursor, row):
    return {col[0]: row[idx] for (idx, col) in enumerate(cursor.description)}

class DbResource(Resource):

    __conn = None
    @property
    def conn(self):
        def opendb():
            self.__conn = sqlite3.connect("data.db")
            self.__conn.row_factory = dict_factory
        if self.__conn is None:
            opendb()
        else:
            try:
                self.__conn.total_changes
            except sqlite3.ProgrammingError:
                opendb()
        return self.__conn


class Item(DbResource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank! It should be float."
    )


    def find_by_name(self, name):
        cur = self.conn.cursor()
        res = cur.execute("SELECT * FROM items WHERE name=? LIMIT 1", (name,))
        row = res.fetchone()
        self.conn.close()
        return row

    def upsert(self, name):
        data = self.parser.parse_args()
        self.conn.execute(
                "INSERT OR REPLACE INTO items (name, price) VALUES (?, ?)", (name, data["price"]))
        self.conn.commit()
        self.conn.close()

    @jwt_required()
    def get(self, name):

        row = self.find_by_name(name)
        if row:
            return {"item": row}
        return {"message": "Item '%s' not found." % name}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": "the item with the name '%s' already exists." % name}, 400
        try:
            self.upsert(name)
        except Exception as e:
            return {"message": "Error occured: %s" % e}, 500
        return self.find_by_name(name), 201

    @jwt_required()
    def put(self, name):
        try:
            self.upsert(name)
        except Exception as e:
            return {"message": "Error occured: %s" % e}, 500
        return self.find_by_name(name)

    @jwt_required()
    def delete(self, name):
        self.conn.execute("DELETE FROM items WHERE name=?", (name,))
        self.conn.close()
        return {"message": "Item '%s' deleted." % name}

class ItemList(DbResource):
    @jwt_required()
    def get(self):
        items = self.conn.execute("SELECT * FROM items").fetchall()
        self.conn.close()
        return {"items": items}


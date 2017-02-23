import sqlite3
from flask_restful import Resource, reqparse
from security import authenticate, identity
from flask_jwt import jwt_required

def find_item(name):
    return next(filter(lambda i: i.get("name") == name, items), None)

def dict_factory(cursor, row):
    return {col[0]: row[idx] for (idx, col) in enumerate(cursor.description)}

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank! It should be float."
    )

    __conn = None
    @property
    def conn(self):
        if self.__conn is None:
            self.__conn = sqlite3.connect("data.db")
            self.__conn.row_factory = dict_factory
        else:
            try:
                self.__conn.total_changes
            except sqlite3.ProgrammingError:
                self.__conn = sqlite3.connect("data.db")
                self.__conn.row_factory = dict_factory
        return self.__conn

    def find_by_name(self, name):
        cur = self.conn.cursor()
        res = cur.execute("SELECT * FROM items WHERE name=? LIMIT 1", (name,))
        row = res.fetchone()
        self.conn.close()
        return row

    @jwt_required()
    def get(self, name):

        row = self.find_by_name(name)
        if row:
            return {"item": row}
        return {"message": "Item '%s' not found." % name}, 400

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": "the item with the name '%s' already exists." % name}, 400
        data = self.parser.parse_args()
        self.conn.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, data["price"]))
        self.conn.commit()
        self.conn.close()

        return self.find_by_name(name), 201

    @jwt_required()
    def put(self, name):
        item = find_item(name)
        data = self.parser.parse_args()
        if item is None:
            item = dict(name=name, price=data.get("price"))
            items.append(item)
        else:
            item.update(data)
        return item

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda i: i.get("name") != name, items))
        return {"message": "Item '%s' deleted." % name}

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": items}


from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "%*R)(FJ)W$J)$JR)J)WU$"
api = Api(app)

jwt = JWT(app, authenticate, identity) ## creates a new endpoint /auth

items = []

def find_item(name):
    return next(filter(lambda i: i.get("name") == name, items), None)

class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = find_item(name)
        return {"item": item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if find_item(name):
            return {"message": "the item with the name '%s' already exists." % name}, 400
        data = request.get_json(force=True, silent=True)
        item = dict(name=name, price=data.get("price"))
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda i: i.get("name") != name, items))
        return {"message": "Item '%s' deleted." % name}

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

if __name__ == "__main__":
    app.run(port=5000, debug=True)


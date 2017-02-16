from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


items = []

def find_item(name):
    return next(filter(lambda i: i.get("name") == name, items), None)

class Item(Resource):

    def get(self, name):
        item = find_item(name)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if find_item(name):
            return {"message": "the item with the name '%s' already exists." % name}, 400
        data = request.get_json(force=True, silent=True)
        item = dict(name=name, price=data.get("price"))
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {"items": items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

if __name__ == "__main__":
    app.run(port=5000, debug=True)


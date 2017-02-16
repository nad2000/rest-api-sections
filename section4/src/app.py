from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


items = []

class Item(Resource):

    def get(self, name):
        for i in items:
            if i.get("name") == name:
                return i
        else:
            return {"error": "Item '%s' not found" % name}, 404

    def post(self, name):
        item = {"name": name, "price": 12.99}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {"items": items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

if __name__ == "__main__":
    app.run(port=5000, debug=True)


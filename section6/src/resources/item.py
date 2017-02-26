from flask_restful import Resource, reqparse
from security import authenticate, identity
from flask_jwt import jwt_required
from models.item import Item as ItemModel
from models.item import ItemList as ItemListModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank! It should be float."
    )


    def find_by_name(self, name):
        return ItemModel.find_by_name(name)

    def insert_or_update(self, name):
        data = self.parser.parse_args()
        return {"item": ItemModel.upsert(name, data["price"])}

    @jwt_required()
    def get(self, name):

        row = ItemModel.find_by_name(name)
        if row:
            return {"item": row}
        return {"message": "Item '%s' not found." % name}, 404

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {"message": "the item with the name '%s' already exists." % name}, 400
        try:
            item = self.insert_or_update(name)
        except Exception as e:
            return {"message": "Error occured: %s" % e}, 500
        else:
            return item, 201

    @jwt_required()
    def put(self, name):
        try:
            item = self.insert_or_update(name)
        except Exception as e:
            return {"message": "Error occured: %s" % e}, 500
        else:
            return item

    @jwt_required()
    def delete(self, name):
        ItemModel.delete(name)
        return {"message": "Item '%s' deleted." % name}

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": ItemListModel.get_items()}


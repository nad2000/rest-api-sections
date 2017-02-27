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


    def insert_or_update(self, name):
        data = self.parser.parse_args()
        item = ItemModel(name, data["price"])
        item.upsert()
        return item

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return {"item": item.to_dict()}
        return {"message": "Item '%s' not found." % name}, 404

    @jwt_required()
    def post(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            return {"message": "the item with the name '%s' already exists." % name}, 400
        try:
            item = self.insert_or_update(name)
        except Exception as e:
            return {"message": "Error occured: %s" % e}, 500
        else:
            return {"item": item.to_dict()}, 201

    @jwt_required()
    def put(self, name):
        try:
            item = self.insert_or_update(name)
        except Exception as e:
            return {"message": "Error occured: %s" % e}, 500
        else:
            return {"item": item.to_dict()}

    @jwt_required()
    def delete(self, name):
        ItemModel(name=name).delete()
        return {"message": "Item '%s' deleted." % name}

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": ItemListModel.get_items()}


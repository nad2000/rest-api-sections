from flask_restful import Resource, reqparse
from security import authenticate, identity
from flask_jwt import jwt_required
from models.item import Item

class ItemResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
            type=float,
            required=True,
            help="This field cannot be left blank! It should be float."
    )
    parser.add_argument("store_id",
            type=int,
            required=True,
            help="The store_id field cannot be left blank! It should be int."
    )

    def insert_or_update(self, name):
        data = self.parser.parse_args()
        store_id = data.get("store_id")
        item = Item(name, data["price"], store_id)
        item.save()
        return item

    @jwt_required()
    def get(self, name):

        item = Item.find_by_name(name)
        if item:
            return {"item": item.to_dict()}
        return {"message": "Item '%s' not found." % name}, 404

    @jwt_required()
    def post(self, name):

        try:
            item = Item.find_by_name(name)
            if item:
                return {"message": "the item with the name '%s' already exists." % name}, 400
            item = self.insert_or_update(name)
        except Exception as ex:
            return {"message": "Error occured: %s" % ex}, 500
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
        item = Item.find_by_name(name)
        if item:
            item.delete()

        return {"message": "Item '%s' deleted." % name}

class ItemListResource(Resource):
    @jwt_required()
    def get(self):
        return {"items": [i.to_dict() for i in Item.get_items()]}


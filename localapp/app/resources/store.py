from flask_jwt import jwt_required
from flask_restful import Resource
from models.store import Store

class StoreResource(Resource):

    @jwt_required()
    def get(self, name):
        store = Store.find_by_name(name)
        if store:
            return store.to_dict()
        return {"message": "Store %s not found" % name}, 404

    @jwt_required()
    def post(self, name):
        if Store.find_by_name(name):
            return {"message": "A store %s already exists" % name}, 400
        store = Store(name)
        try:
            store.save()
        except Exception as ex:
            return dict(message="An error occured while creating the store: %s" % ex), 500 

        return store.to_dict(), 201

    @jwt_required()
    def delete(self, name):
        store = Store.find_by_name(name)

        if store:
            store.delete_from_db()
        return dict(message="The store '%s' was deleted." % name)

class StoreListResource(Resource):
    @jwt_required()
    def get(self):

        return dict(stores=[s.to_dict() for s in Store.get_items()])

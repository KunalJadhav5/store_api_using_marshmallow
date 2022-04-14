from flask_restful import Resource
from models.store import StoreModel
from db import db
from schemas.store import StoreSchema

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    def get(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        return {'message': 'Store not found'}, 400

    @classmethod
    def post(cls, name):
        if StoreModel.find_by_name(name):
            return {"message": "Store already exist"},400
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred"}, 500
        return store_schema.dump(store),201

    @classmethod
    def delete(cls, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete()

        return {"message": "Deleted"}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"store": store_list_schema.dump(StoreModel.find_all())}
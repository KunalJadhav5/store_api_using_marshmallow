import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from schemas.item import ItemSchema
from flask import request
from marshmallow import ValidationError

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_username(name)
        if item:
            return item_schema.dump(item)
        return {"message": "Item not found"}

    def post(self, name):
        if ItemModel.find_by_username(name):
            return {'message': "Item {} already exist".format(name)}, 400
        item_json = request.get_json()
        print(item_json)
        item_json['name'] = name
        try:
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 404

        try:
            item.save_to_db()
        except Exception as e:
            return {"message":"An error occurred"}, 500
        return item_schema.dump(item), 201

    def delete(self, name):
        item = ItemModel.find_by_username(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        item_json = request.get_json()
        item = ItemModel.find_by_username(name)
        if item:
            item.price = item_json['price']

        else:
            print(item_json)
            item_json['name'] = name
            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 404

        item.save_to_db()

        return item_schema.dump(item)


class ItemList(Resource):
    def get(self):
        return {'items': item_list_schema.dump(ItemModel.find_all())}


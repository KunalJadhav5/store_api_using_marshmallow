import sqlite3
from flask_restful import reqparse, Resource
from flask import request
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import ValidationError
user_schema = UserSchema()


class UserRegistration(Resource):

    def post(self):
        try:
            user = user_schema.load(request.get_json())
            print(user)
        except ValidationError as err:
            return err.messages, 400
        if UserModel.find_by_username(user.username):
            return {"message": "User already exist"}
        user.save_to_db()

        return {'message': "User created successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return "User not found", 404
        return user_schema.dump(user), 200

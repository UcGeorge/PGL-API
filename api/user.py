from flask_restful import Resource, abort, marshal_with, fields
from model.user_model import UserModel
from app import db

mfields = {
    'name': fields.String
}


class User(Resource):

    @marshal_with(mfields)
    def get(self, username: str):
        result = UserModel.query.get(username.lower())
        if not result:
            abort(404, message='User does not exist')
        return result

    @marshal_with(mfields)
    def put(self, username: str):
        result = UserModel.query.get(username.lower())
        if result:
            abort(409, message='User already exists')
        user = UserModel(name=username.lower())
        db.session.add(user)
        db.session.commit()
        return user, 201

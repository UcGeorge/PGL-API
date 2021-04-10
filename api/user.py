from flask_restful import Resource, abort, marshal_with, fields
from model.user_model import user
from app import db

mfields = {
    'name': fields.String
}


class User(Resource):

    @marshal_with(mfields)
    def get(self, username: str):
        result = user.query.get(username.lower())
        if not result:
            abort(404, message=f'{username} does not exist')
        return result

    @marshal_with(mfields)
    def put(self, username: str):
        result = user.query.get(username.lower())
        if result:
            abort(409, message=f'{username} already exists')
        new_user = user(name=username.lower())
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

from flask_restful import Resource, abort, marshal_with, fields, reqparse
from model.user_model import user
from model.user_novel_model import user_novel
from model.novel_model import novel
from app import db

getReadsFields = {
    'id': fields.Integer,
    'name': fields.String
}

putReadArgs = reqparse.RequestParser()
putReadArgs.add_argument('novel_id', type=int,
                         help='id of novel is required', required=True)


class Reads(Resource):

    @marshal_with(getReadsFields)
    def get(self, username: str):
        result = user.query.get(username.lower())
        if not result:
            abort(404, message=f'{username} does not exist')

        sel = user_novel.select().where(user_novel.c.username == username)

        user_novels = db.engine.execute(sel)

        d, a = {}, []
        for rowproxy in user_novels:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        if a == []:
            abort(404, message=f'User has no novels')
        else:
            result = [novel.query.get(x['novel_id']) for x in a]

        return result

    @marshal_with(getReadsFields)
    def put(self, username: str):
        args = putReadArgs.parse_args()
        the_user = user.query.get(username.lower())
        the_novel = novel.query.get(args['novel_id'])
        if not (the_user and the_novel):
            abort(
                409, message=f"{username if not the_user else args['novel_id']} doesn't exist")

        sel = user_novel.select().where(user_novel.c.username == username)

        user_novels = db.engine.execute(sel)

        d, a = {}, []
        for rowproxy in user_novels:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        if the_novel.id in [x['novel_id'] for x in a]:
            abort(401, message=f"This novel is already part of the user's collection")

        ins = user_novel.insert().values(
            username=username, novel_id=args['novel_id'])
        db.engine.execute(ins)
        return the_novel, 201

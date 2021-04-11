from flask_restful import Resource, abort, marshal_with, fields, reqparse
from model.user_model import user
from model.user_novel_model import user_novel
from model.novel_model import novel
from app import db, helper

getReadsFields = {
    'name': fields.String
}

putReadArgs = reqparse.RequestParser()
putReadArgs.add_argument('novel_name', type=str,
                         help='name of novel is required', required=True)


class Reads(Resource):

    @marshal_with(getReadsFields)
    def get(self, username: str):
        result = user.query.get(helper.str_to_id(username))
        if not result:
            abort(404, message=f'{username} does not exist')

        sel = user_novel.select().where(user_novel.c.username == helper.str_to_id(username))

        sql_res = db.engine.execute(sel)

        user_novels = helper.parse_ResultProxy(sql_res)

        if user_novels == []:
            abort(404, message=f'User has no novels')
        else:
            result = [novel.query.get(helper.str_to_id(
                x['novel_name'])) for x in user_novels]

        return result

    @marshal_with(getReadsFields)
    def put(self, username: str):
        args = putReadArgs.parse_args()
        the_user = user.query.get(helper.str_to_id(username))
        the_novel = novel.query.get(helper.str_to_id(args['novel_name']))
        if not (the_user and the_novel):
            abort(
                409, message=f"{username if not the_user else args['novel_name']} doesn't exist")

        sel = user_novel.select().where(user_novel.c.username == helper.str_to_id(username))
        sql_res = db.engine.execute(sel)
        user_novels = helper.parse_ResultProxy(sql_res)

        if the_novel.name in [x['novel_name'] for x in user_novels]:
            abort(401, message=f"This novel is already part of the user's collection")

        ins = user_novel.insert().values(
            username=helper.str_to_id(username),
            novel_name=helper.str_to_id(args['novel_name'])
        )
        db.engine.execute(ins)
        return the_novel, 201

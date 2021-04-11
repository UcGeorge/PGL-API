from app import db, helper
from model.novel_model import novel
from flask_restful import Resource, abort, marshal_with, fields, reqparse

getFields = {
    'name': fields.String
}

putNovelArgs = reqparse.RequestParser()
putNovelArgs.add_argument('name', type=str,
                          help='Name of novel is required', required=True)

getNovelArgs = reqparse.RequestParser()
getNovelArgs.add_argument('name', type=str,
                          help='name of novel is required')


class Novel(Resource):

    def get_single(self, name: str):
        result = novel.query.get(helper.str_to_id(name))
        if not result:
            abort(404, message=f'{name} does not exist')
        return result

    @marshal_with(getFields)
    def get(self):
        args = getNovelArgs.parse_args()

        if args['name'] is not None:
            return self.get_single(args['name'])

        result = novel.query.order_by(novel.name).all()
        if result == [] or result is None:
            abort(404, message='There are no novels')
        return result

    @marshal_with(getFields)
    def put(self):

        args = putNovelArgs.parse_args()
        the_novel = novel.query.get(helper.str_to_id(args['name']))

        if the_novel:
            abort(401, message=f"{args['name']} already exists")

        new_novel = novel(name=helper.str_to_id(args['name']))
        db.session.add(new_novel)
        db.session.commit()
        return args, 201

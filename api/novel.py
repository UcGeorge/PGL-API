from app import db
from model.novel_model import novel
from flask_restful import Resource, abort, marshal_with, fields, reqparse

getFields = {
    'id': fields.Integer,
    'name': fields.String
}

putNovelArgs = reqparse.RequestParser()
putNovelArgs.add_argument('id', type=int,
                          help='id of novel is required', required=True)
putNovelArgs.add_argument('name', type=str,
                          help='Name of novel is required', required=True)

getNovelArgs = reqparse.RequestParser()
getNovelArgs.add_argument('id', type=int,
                          help='id of novel is required')


class Novel(Resource):

    def get_single(self, id):
        result = novel.query.get(id)
        if not result:
            abort(404, message=f'novel with id: {id} does not exist')
        return result

    @marshal_with(getFields)
    def get(self):
        args = getNovelArgs.parse_args()

        if args['id'] is not None:
            return self.get_single(args['id'])

        result = novel.query.order_by(novel.id).all()
        if result == [] or result is None:
            abort(404, message='There are no novels')
        return result

    @marshal_with(getFields)
    def put(self):

        args = putNovelArgs.parse_args()
        the_novel = novel.query.get(args['id'])

        if the_novel:
            abort(401, message=f"novel with id: {args['id']} already exists")

        new_novel = novel(id=args['id'], name=args['name'])
        db.session.add(new_novel)
        db.session.commit()
        return the_novel, 201

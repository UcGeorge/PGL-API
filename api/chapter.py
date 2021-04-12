from operator import index
from model.novel_model import novel
from flask_restful import Resource, abort, marshal_with, fields, reqparse
from model.chapter_model import chapter
from app import db, helper

mfields = {
    'index': fields.String,
    'name': fields.String,
    'novel': fields.String,
}

putChapterArgs = reqparse.RequestParser()
putChapterArgs.add_argument('name', type=str,
                            help='Name of chapter is required', required=True)
putChapterArgs.add_argument('content', type=str,
                            help='Content of chapter is required', required=True)

getChapterArgs = reqparse.RequestParser()
getChapterArgs.add_argument('name', type=str)


class Chapter(Resource):

    @marshal_with(mfields)
    def get(self, novel_name: str):
        args = getChapterArgs.parse_args()
        if args['name']:
            result = chapter.query.filter_by(
                name=args['name']).first()
            if not result or result == []:
                abort(
                    404, message=f"{args['name']} not found for {novel_name}")
        else:
            result = chapter.query.filter_by(
                novel_name=helper.str_to_id(novel_name)).all()
            if not result or result == []:
                abort(404, message=f'No chapters for {novel_name}')
        return result

    @marshal_with(mfields)
    def put(self, novel_name: str):
        args = putChapterArgs.parse_args()

        q_novel = novel.query.get(helper.str_to_id(novel_name))

        if not q_novel:
            abort(409, message=f'{novel_name} does not exist')

        novel_chapters = [(int(chapter.index.replace(helper.str_to_id(novel_name) + '-', '')), chapter.name)
                          for chapter in chapter.query.filter_by(novel_name=helper.str_to_id(novel_name)).order_by(chapter.index).all()]

        if args['name'] in (x[1] for x in novel_chapters):
            abort(401, message=f"{args['name']} already exists")

        last_index = 0 if novel_chapters == None or novel_chapters == [
        ] else max((x[0] for x in novel_chapters))
        new_index = f"{helper.str_to_id(novel_name)}-{last_index+1}"

        new_chapter = chapter(
            index=helper.str_to_id(new_index),
            name=args['name'],
            content=args['content'],
            novel_name=helper.str_to_id(novel_name)
        )
        db.session.add(new_chapter)
        db.session.commit()
        return new_chapter, 201

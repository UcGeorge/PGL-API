from flask_restful import Resource


class Hello(Resource):
    def get(self):
        return {"data": "Hi, You are connected"}

from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
db = SQLAlchemy()

if True:
    from model import (chapter_model, novel_model, user_model)

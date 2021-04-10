from model.novel_model import NovelModel
from app import db


class UserModel(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    novels = db.relationship('NovelModel', secondary=NovelModel,
                             lazy='subquery', backref=db.backref('users', lazy=True))

    def __repr__(self) -> str:
        return f"User(Name = {self.name})"

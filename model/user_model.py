from model.user_novel_model import user_novel
from app import db


class user(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    novels = db.relationship('novel', secondary=user_novel,
                             lazy='subquery', backref=db.backref('user', lazy=True))

    def __repr__(self) -> str:
        return f"User(Name = {self.name})"

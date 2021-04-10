from app import db


class NovelModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    chapters = db.relationship('ChapterModel', backref='novelmodel', lazy=True)

    def __repr__(self) -> str:
        return f"User(id = {self.id}, Name = {self.name})"

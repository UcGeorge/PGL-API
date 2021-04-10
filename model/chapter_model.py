from app import db


class ChapterModel(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey(
        'novelmodel.id'), nullable=False)

    def __repr__(self) -> str:
        return f"User(Name = {self.name})"

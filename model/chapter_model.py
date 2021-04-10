from app import db


class chapter(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey(
        'novel.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Chapter(Name = {self.name}, Novel = {self.novel_id})"

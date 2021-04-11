from app import db


class chapter(db.Model):
    index = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    novel_name = db.Column(db.String(80), db.ForeignKey(
        'novel.name'), nullable=False)

    def __repr__(self) -> str:
        return f"Chapter(Name = {self.name}, Novel = {self.novel_name})"

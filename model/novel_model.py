from app import db


class novel(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    chapters = db.relationship('chapter', backref='novel', lazy=True)

    def __repr__(self) -> str:
        return f"Novel(Name = {self.name})"

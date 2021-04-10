from app import db


class novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    chapters = db.relationship('chapter', backref='novel', lazy=True)

    def __repr__(self) -> str:
        return f"Novel(id = {self.id}, Name = {self.name})"

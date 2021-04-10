from app import db


user_novel = db.Table(
    'user_novel',
    db.Column('username', db.String(80), db.ForeignKey(
        'usermodel.name'), primary_key=True),
    db.Column('novel_id', db.Integer, db.ForeignKey(
        'novelmodel.id'), primary_key=True)
)

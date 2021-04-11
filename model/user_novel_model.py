from app import db


user_novel = db.Table(
    'user_novel',
    db.Column('username', db.String(80), db.ForeignKey(
        'user.name')),
    db.Column('novel_name', db.String(80), db.ForeignKey(
        'novel.name'))
)

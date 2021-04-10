from api import user, hello, reads
from flask import Flask
from app import db, api


app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

with app.app_context():
    db.create_all()

# Add resources
api.add_resource(hello.Hello, '/hello')
api.add_resource(user.User, '/user/<string:username>')
api.add_resource(reads.Reads, '/reads/<string:username>')

# Initialize this class with the given flask application
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL, create_engine
from sqlalchemy_utils import database_exists, create_database
from config import (DB_HOST, DB_NAME, DB_PORT, DB_SUPERUSER_USERNAME, DB_SUPERUSER_PASSWORD)


DB_URL = f'postgresql://{"postgres"}:{DB_SUPERUSER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DB_URL)
if not database_exists(DB_URL):
    create_database(engine.url)

# 'sqlite:///:memory:'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


with app.app_context():
    db.create_all()


# Resource for handling user operations
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {'username': user.username, 'email': user.email}
        else:
            return {'message': 'User not found'}, 404

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        print(db)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


api.add_resource(UserResource, '/users/<int:user_id>', '/users')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask_restful import Api
from app.urls import add_urls
from config import SECRET_KEY, DB_URL
from app.database.models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    # db.init_app(app)

    return app


def init_db(app):
    return db.init_app(app)


def create_api(app):
    api = Api(app)
    return api


if __name__ == '__main__':
    app = create_app()
    init_db(app)
    api = create_api(app)
    add_urls(api)
    app.run(debug=True)

# result = db.session.query(GroupModel.group_name).all()
# print(result)






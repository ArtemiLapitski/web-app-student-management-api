from flask import Flask
from flask_restful import Api
from app.urls import add_urls
from config import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    return app


def create_api(app):
    api = Api(app)
    return api


if __name__ == '__main__':
    app = create_app()
    api = create_api(app)
    add_urls(api)
    app.run(debug=True)







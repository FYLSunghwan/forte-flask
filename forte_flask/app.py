from flask import Flask
from .views.routes import routes_blueprint

def create_app():
    """Creates Flask App

    :return: Flask App
    """
    app = Flask(__name__)
    app.register_blueprint(routes_blueprint)

    return app
from flask import Blueprint, render_template

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route("/")
def index():
    return "Test Routing"
import subprocess
import os
from flask import Blueprint, request, jsonify

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route("/")
def index():
    return "Test Routing"

@routes_blueprint.route("/audiveris")
def audiveris():
    if request.method == 'POST':
        #file = request.files['file']
        #file.save('test')
        #subprocess.call(["sudo","docker","run","toprock/audiveris"])
        return 'success'
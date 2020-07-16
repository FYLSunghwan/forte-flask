import subprocess
import os
from flask import Blueprint, request, jsonify
from werkzeug import secure_filename

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route("/")
def index():
    return "Test Routing"

@routes_blueprint.route("/audiveris", methods = ['POST'])
def audiveris():
    if request.method == 'POST':
        file = request.files['file']
        file.save("./test/"+secure_filename(file.filename))
        #subprocess.call(["sudo","docker","run","toprock/audiveris"])
        return 'success'
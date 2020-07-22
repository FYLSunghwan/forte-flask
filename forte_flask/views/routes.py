import json
import os
from flask import Blueprint, request, jsonify, send_file
from werkzeug import secure_filename
from forte_flask.engines.omr import audiveris

# Routes Blueprint from Flask
routes_blueprint = Blueprint('routes', __name__)
root_dir = os.getcwd()

@routes_blueprint.route("/")
def index():
    return "Test Routing"

@routes_blueprint.route("/omr-convert", methods = ['POST'])
def omr_convert():
    if request.method == 'POST':
        user_id = request.form['id']
        file = request.files['file']

        """
            User Directory : {ProjectDirectory}/omrdata/user_id
            Input Directory : {UserDirectory}/inputs
            Output Directory : {UserDirectory}/outputs
        """
        user_dir = os.path.join(root_dir, 'omr_data', user_id)
        input_dir = os.path.join(user_dir, 'inputs')
        output_dir = os.path.join(user_dir, 'outputs')

        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_path = os.path.join(input_dir, secure_filename(file.filename))
        file.save(file_path)

        audiveris(input_dir, output_dir)
        filename_without_ext = os.path.splitext(file.filename)[0]
        out_path = os.path.join(output_dir, filename_without_ext, filename_without_ext+".mxl")

        if os.path.exists(out_path):
            return jsonify({'message':'success', 'filename':filename_without_ext})

        return jsonify({'message':'fail'})

@routes_blueprint.route("/omr-get/<string:user_id>/<string:filename>")
def omr_get(user_id,filename):
    out_dir = os.path.join(root_dir, 'omr_data', user_id, 'outputs', filename, filename+'.mxl')
    if not os.path.exists(out_dir):
        return jsonify({'message':'fail'})
    return send_file(out_dir, as_attachment=True)
    
import os
import random
import string

from flask import request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename

from . import files_bp

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({ 'error' :'No selected file'}), 400
    if file and allowed_file(file.filename):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        filename = f"{random_string}_{secure_filename(file.filename)}"
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({ "file_url": f"/files/download/{filename}"},201)



@files_bp.route('/download/<file_key>', methods=['GET'])
def download_file(file_key):
    if file_key and allowed_file(file_key):
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], file_key)


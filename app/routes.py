import os
from flask import Blueprint, request, jsonify

UPLOAD_FOLDER = 'csv-uploads'
ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('main', __name__)
bp.config = {}

@bp.route('/')
def index():
    return 'Index page'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/uploadCsv', methods=['POST'])
def upload_csv():
    if 'csv' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['csv']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Guarda el archivo en el servidor
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # Devuelve la ruta del archivo guardado
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        return jsonify({'file_path': file_path}), 201
    
    return jsonify({'error': 'File not allowed'}), 400



    
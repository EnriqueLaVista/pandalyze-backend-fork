import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from io import TextIOWrapper
from ..services.csv_service import save_csv_data, get_csv_by_content

bp = Blueprint('save_csv', __name__)

MAX_CONTENT_LENGTH_IN_BYTES = 10 * 1024 * 1024 # Tamaño maximo del csv: 10Mb
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/uploadCsv', methods=['POST'])
def upload_csv():
    file = request.files['csv']

    if not file:
        return jsonify({'error': 'No file part'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        file.seek(0, os.SEEK_END)
        file_size = file.tell()

        file.seek(0)
        
        if file_size > MAX_CONTENT_LENGTH_IN_BYTES:
            return jsonify({'error': 'El archivo CSV supera los 10 megabytes'}), 400
        
        filename = secure_filename(file.filename)
        
        csv_content = TextIOWrapper(file, encoding='utf-8-sig').read()
        csv_id, columns_names = get_csv_by_content(csv_content)
        
        # Si no existe el csv en la BD, lo guardamos.
        # El criterio para definir si "existe" el csv es el campo "data" que representa el cuerpo del csv
        if not csv_id:
            csv_id, columns_names = save_csv_data(filename, csv_content)

        return jsonify({'fileName': filename, 'csvId': csv_id, 'columnsNames': columns_names}), 201
    
    return jsonify({'error': 'File not allowed'}), 400
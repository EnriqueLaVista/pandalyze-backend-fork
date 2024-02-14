import os, json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'csv-uploads'
ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('main', __name__)
bp.config = {}

@bp.route('/')
def index():
    return 'Index page'

@bp.route('/run_python_code', methods=['POST'])
def run_python_code():
    if 'code' not in request.json:
        return jsonify({'error': 'No se proporcionó ningún código Python'}), 400
    
    code = request.json['code']
    
    try:
        # Ejecuta el código Python proporcionado
        exec_result = {}
        exec(f"result = {code}", {}, exec_result)
        
        # Captura el resultado
        result = exec_result.get('result', None)

        # Devuelve el resultado como parte de la respuesta JSON
        if result is not None:
            return jsonify({'result': result}), 200
        else:
            return jsonify({'info': 'No se encontró ningún resultado'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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



    
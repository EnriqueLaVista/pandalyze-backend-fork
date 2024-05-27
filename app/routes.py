import sys
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from io import StringIO, TextIOWrapper
from .services.csv_service import save_csv_data, read_csv, get_csv_by_filename
import pandas as pandas
import plotly.express as plotly
import plotly.io as pio
from .services.error_formatter_service import ExceptionFormatter


ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return 'Index page'

@bp.route('/runPythonCode', methods=['POST'])
def run_code():
    if 'code' not in request.json:
        return jsonify({'error': 'No se proporcionó ningún código Python'}), 400
    
    code = request.json['code']    
    
    try:
        json_plots = []
        
        # Temporalmente cambiamos la salida estandar a una variable 'output'
        output = StringIO()
        sys.stdout = output
        exec_globals = {'read_csv': read_csv, 'plotly': plotly, 'pio': pio, '_jsonPlots_': json_plots}
        exec(code, exec_globals)
        
        # Restaura la salida estándar a la consola
        sys.stdout = sys.__stdout__
        
        # Obtiene la salida capturada
        output_value = output.getvalue()

        return jsonify({'output': output_value, 'plots': json_plots}), 200
    except Exception as e:
        # Restaura la salida estándar a la consola
        sys.stdout = sys.__stdout__
    
        # Formateamos la excepcion para que sea mas legible
        personalized_error, original_error = ExceptionFormatter.get_error_messages(e)
        print({'Excepcion al correr codigo': e})
        return jsonify({'personalized_error': personalized_error, 'original_error': original_error}), 500

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
        filename = secure_filename(file.filename)
        
        csv_id, columns_names = get_csv_by_filename(filename)
        
        # Chequea que ya exita en la BD por el filename
        if not csv_id:
            # Lee y almacena la información del CSV en la base de datos
            csv_content = TextIOWrapper(file, encoding='utf-8-sig').read()
            csv_id, columns_names = save_csv_data(filename, csv_content)

        return jsonify({'fileName': filename, 'csvId': csv_id, 'columnsNames': columns_names}), 201
    
    return jsonify({'error': 'File not allowed'}), 400
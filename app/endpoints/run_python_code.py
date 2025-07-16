from flask import Blueprint, request
import sys, threading, re
from flask import Blueprint, request, jsonify
from io import StringIO
from ..services.csv_service import read_csv
import pandas as pandas
import plotly.express as plotly
import plotly.io as pio
from flask_cors import cross_origin
from ..services.error_formatter_service import ExceptionFormatter

bp = Blueprint('run_python_code', __name__)

# Expresiones regulares para buscar estructuras de control y sentencias de import
control_structures_regex = re.compile(r'\b(if|else|elif|for|while|try|except|finally)\b')
import_statement_regex = re.compile(r'\bimport\b')

# Verifica que el codigo sea relativamente esguro. TODO: mejorar esto porque es un parche
def is_safe_code(code):
    if control_structures_regex.search(code):
        return False
    if import_statement_regex.search(code):
        return False
    return True

def execute_code(code, globals_dict, timeout=15):
    exception_list = []
    def exec_wrapper(code, globals_dict):
        from run import app
        try:
            with app.app_context():
                exec(code, globals_dict)
        except Exception as e:
            exception_list.append(e)

    exec_thread = threading.Thread(target=exec_wrapper, args=(code, globals_dict))
    exec_thread.start()
    exec_thread.join(timeout)

    if exec_thread.is_alive():
        raise TimeoutError("Timeout de ejecución excedido (más de {} segundos)".format(timeout))

    if exception_list:
        # Si hay alguna excepción capturada en exec_wrapper, lanzarla nuevamente
        raise exception_list[0]
    
@bp.route('/runPythonCode', methods=['POST'])
@cross_origin()
def run_code():
    code = request.json['code']

    try:
        if not is_safe_code(code):
            raise ValueError("El código contiene sentencias no permitidas")

        # Configuración de pandas para que se imprima mejor
        pandas.options.display.max_columns = None
        pandas.set_option('display.max_colwidth', 20)
        pandas.set_option('display.colheader_justify', 'center')
        pandas.set_option('display.width', 9999)

        json_plots = []
        output = StringIO()
        sys.stdout = output

        # Ejecución del código con chequeos y timeout
        exec_globals = {'read_csv': read_csv, 'plotly': plotly, 'pio': pio, '_jsonPlots_': json_plots}
        execute_code(code, exec_globals)

        # Restaurar salida estándar
        sys.stdout = sys.__stdout__
        output_value = output.getvalue()

        return jsonify({'output': output_value, 'plots': json_plots}), 200

    except Exception as e:
        # Restaura la salida estándar
        sys.stdout = sys.__stdout__
    
        # Formateamos la excepcion para que sea legible para usuarios no experimentados
        personalized_error, original_error = ExceptionFormatter.get_error_messages(e)
        print({'Excepcion al correr codigo': e})
        return jsonify({'personalized_error': personalized_error, 'original_error': original_error}), 500
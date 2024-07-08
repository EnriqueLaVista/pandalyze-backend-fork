from flask import Blueprint, request
import sys
from flask import Blueprint, request, jsonify
from io import StringIO
from ..services.csv_service import read_csv
import pandas as pandas
import plotly.express as plotly
import plotly.io as pio
from ..services.error_formatter_service import ExceptionFormatter

bp = Blueprint('run_python_code', __name__)

@bp.route('/runPythonCode', methods=['POST'])
def run_code():
    code = request.json['code']    
    
    try:
        # Configuraciones generales para el print del dataframe:
        pandas.options.display.max_columns = None
        pandas.set_option('display.max_colwidth', 20)  # Tamaño máximo de cada celda: 20 caracteres
        pandas.set_option('display.colheader_justify', 'center')  # Alinear encabezados de columna al centro
        pandas.set_option('display.width', 9999) # Tamaño total del dataframe (un valor alto evita las elipsis y muestra todas las columnas)

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
    
        # Formateamos la excepcion para que sea legible para usuarios no experimentados
        personalized_error, original_error = ExceptionFormatter.get_error_messages(e)
        print({'Excepcion al correr codigo': e})
        return jsonify({'personalized_error': personalized_error, 'original_error': original_error}), 500
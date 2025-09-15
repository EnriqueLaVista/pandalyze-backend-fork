import traceback
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys, threading, re, pandas, io
import plotly.express as plotly
import plotly.io as pio
import folium  
from ..services.csv_service import read_csv
from ..services.error_formatter_service import ExceptionFormatter
from ..endpoints.map_visualization import generate_map

bp = Blueprint('run_python_code', __name__)

control_structures_regex = re.compile(r'\b(if|else|elif|for|while|try|except|finally)\b')
import_statement_regex = re.compile(r'\bimport\b')

def is_safe_code(code):
    if control_structures_regex.search(code):
        return False
    if import_statement_regex.search(code):
        return False
    return True

def execute_code(code, globals_dict, exception_list, timeout=15):
    def exec_wrapper(code, globals_dict):
        from run import app
        try:
            with app.app_context():
                result = eval(code, globals_dict)
                exception_list.append(result)
        except Exception as e:
            exception_list.append(e)

    exec_thread = threading.Thread(target=exec_wrapper, args=(code, globals_dict))
    exec_thread.start()
    exec_thread.join(timeout=timeout)

    if exec_thread.is_alive():
        exception_list.append(TimeoutError("La ejecución del código superó el tiempo límite"))


@bp.route('/runPythonCode', methods=['POST'])
@cross_origin()
def run_code():
    code = request.json['code']
    try:
        # (la configuración de pandas)
        exec_globals = {
            'read_csv': read_csv,
            'plotly': plotly,
            'pio': pio,
            '_jsonPlots_': [],
            'generate_map': generate_map,
        }
        
        exception_or_result_list = []
        execute_code(code, exec_globals, exception_or_result_list)
        
        # (la salida estándar)
        if not exception_or_result_list:
             return jsonify({'error': "El código no produjo ningún resultado o superó el tiempo límite."}), 500

        result_object = exception_or_result_list[0]

        if isinstance(result_object, Exception):
            raise result_object
            
        if isinstance(result_object, folium.Map):
            map_html = result_object._repr_html_()
            return jsonify({'output': map_html, 'type': 'map'})
        elif hasattr(result_object, 'to_json'):
             plot_json = pio.to_json(result_object)
             return jsonify({'output': '', 'plots': [plot_json]}), 200
        else:
             return jsonify({'output': str(result_object), 'plots': []}), 200

    except Exception as e:
        print("--- ERROR CAPTURADO EN EL ENDPOINT ---")
        print(traceback.format_exc())
        print("------------------------------------")
        
        try:
            formatter = ExceptionFormatter(e)
            personalized_exception = formatter.get_personalized_exception()
        except Exception as formatter_error:
            print(f"¡El formateador de excepciones falló!: {formatter_error}")
            personalized_exception = f"Error de ejecución: {str(e)}"
        
        return jsonify({'error': personalized_exception}), 500
        


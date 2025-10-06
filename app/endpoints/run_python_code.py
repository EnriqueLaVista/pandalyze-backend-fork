import traceback
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys, threading, re, pandas, io, ast  
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

def execute_code(code, globals_dict, result_list, timeout=15):
    """
    Ejecuta código de forma segura en un hilo.
    """
    def exec_wrapper(code, globals_dict):
        from run import app
        try:
            with app.app_context():
                # Analizamos el código para ver qué es
                parsed_code = ast.parse(code.strip())
                
                # Si el código es una sola línea que es una expresión (como llamar a generate_map)
                if len(parsed_code.body) == 1 and isinstance(parsed_code.body[0], ast.Expr):
                    # Usamos eval para obtener el objeto que devuelve (el mapa)
                    result = eval(code, globals_dict)
                    result_list.append(result)
                else:
                    # Si es una sentencia (como print) o varias líneas, usamos exec
                    exec(code, globals_dict)
        except Exception as e:
            result_list.append(e)

    exec_thread = threading.Thread(target=exec_wrapper, args=(code, globals_dict))
    exec_thread.start()
    exec_thread.join(timeout=timeout)

    if exec_thread.is_alive():
        result_list.append(TimeoutError("La ejecución del código superó el tiempo límite"))


@bp.route('/runPythonCode', methods=['POST'])
@cross_origin()
def run_code():
    code = request.json['code']
    try:
        if not is_safe_code(code):
            raise ValueError("El código contiene sentencias no permitidas")

        pandas.options.display.max_columns = None
        pandas.set_option('display.max_colwidth', 20)
        pandas.set_option('display.colheader_justify', 'center')
        pandas.set_option('display.width', 9999)

        output_catcher = io.StringIO()
        sys.stdout = output_catcher

        exec_globals = {
            'read_csv': read_csv,
            'plotly': plotly,
            'pio': pio,
            '_jsonPlots_': [], 
            'generate_map': generate_map
        }
        
        result_list = []
        execute_code(code, exec_globals, result_list)
        
        sys.stdout = sys.__stdout__
        text_output = output_catcher.getvalue()

        if not result_list and not text_output:
             return jsonify({'error': "El código no produjo ningún resultado o superó el tiempo límite."}), 500

        result_object = result_list[0] if result_list else None

        if isinstance(result_object, Exception):
            raise result_object
            
        if isinstance(result_object, folium.Map):
            map_html = result_object._repr_html_()
            return jsonify({'output': map_html, 'type': 'map'})
        
        # Si no es un mapa, devolvemos la salida de texto de los print()
        # y los gráficos de plotly si los hubiera.
        return jsonify({'output': text_output, 'plots': exec_globals['_jsonPlots_']}), 200

    except Exception as e:
        sys.stdout = sys.__stdout__
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
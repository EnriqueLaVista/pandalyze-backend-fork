import traceback
import sys, threading, re, pandas, io, ast
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
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
    def exec_wrapper(code, globals_dict):
        from run import app
        try:
            with app.app_context():
                parsed_code = ast.parse(code.strip())

                if len(parsed_code.body) == 1 and isinstance(parsed_code.body[0], ast.Expr):
                    result = eval(code, globals_dict)
                    result_list.append(result)
                else:
                    exec(code, globals_dict)
        except Exception as e:
            result_list.append(e)

    thread = threading.Thread(target=exec_wrapper, args=(code, globals_dict))
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        result_list.append(TimeoutError("La ejecución del código superó el tiempo límite."))


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

        json_plots = []
        original_show = pio.show

        def custom_show(fig, *args, **kwargs):
            plot_json = pio.to_json(fig)
            json_plots.append(plot_json)
        pio.show = custom_show

        exec_globals = {
            'read_csv': read_csv,
            'plotly': plotly,
            'pio': pio,
            'pd': pandas,
            '_jsonPlots_': json_plots,
            'generate_map': generate_map,
        }

        result_list = []
        execute_code(code, exec_globals, result_list)

        sys.stdout = sys.__stdout__
        pio.show = original_show

        text_output = output_catcher.getvalue()
        result_obj = result_list[0] if result_list else None

        if isinstance(result_obj, Exception):
            raise result_obj

        if isinstance(result_obj, folium.Map):
            map_html = result_obj._repr_html_()
            return jsonify({'output': map_html, 'type': 'map'})

        if text_output.strip().startswith("<div id=\"map_"):
            return jsonify({'output': text_output, 'type': 'map'})

        return jsonify({'output': text_output, 'plots': json_plots}), 200

    except Exception as e:
        sys.stdout = sys.__stdout__
        if 'original_show' in locals():
            pio.show = original_show

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

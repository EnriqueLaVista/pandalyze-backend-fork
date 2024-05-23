import traceback
import pandas as pandas
import plotly.express as plotly
import plotly.io as pio
import re

class ExceptionFormatter:
    @staticmethod
    def get_error_messages(excepcion):
        switch = {
            SyntaxError: "Ocurrió un error de sintaxis {}, revisa la estructura de tu código.",
            NameError: "Se ha utilizado una variable no definida {}, revisa tu código.",
            AttributeError: "Se intentó acceder a un atributo que no existe en un objeto {}.",
            TypeError: "Se ha producido un error de tipo {}.",
            ValueError: "Se ha producido un error de valor {}.",
            KeyError: "Se ha intentado acceder a una clave que no existe en un diccionario {}.",
            IndexError: "Se ha intentado acceder a un índice fuera del rango en una lista o tupla {}.",
            FileNotFoundError: "El archivo especificado no se ha encontrado. Revisar {}.",
            pandas.errors.ParserError: "Ocurrió un error al analizar el archivo CSV. Revisar {}.",
            pandas.errors.DtypeWarning: "Advertencia: Ocurrió un problema con los tipos de datos en el archivo CSV, revisar {}.",
            pandas.errors.UnsupportedFunctionCall: "Ocurrió un error al llamar a una función no soportada en DataFrame de pandas, revisar {}.",
            pandas.errors.EmptyDataError: "El DataFrame de pandas está vacío, revisar {}.",
            #falta plotly y pio
        }
        
        # Mensaje genérico por defecto
        default_message = "Ocurrió un error cerca de la ejecución del código {}."

        error_info = traceback.format_exception_only(type(excepcion), excepcion)
        original_error = ''.join(error_info)
        
        error_line_number_text = get_error_line_number_text(original_error)
        personalized_error = switch.get(type(excepcion), default_message).format(error_line_number_text)
      
        return personalized_error, original_error

def get_error_line_number_text(error):
    match = re.search(r'line (\d+)', error)
    if match:
        return "cerca de la línea " + match.group(1)
    else: 
        return ""
import traceback
import pandas as pandas
import plotly.express as plotly
import plotly.io as pio
import re

class ExceptionFormatter:
    errorMessagesMap = {
        SyntaxError: "Ocurrió un error de sintaxis. {}",
        NameError: "Se ha utilizado una variable no definida. {}",
        AttributeError: "Se intentó acceder a un atributo que no existe en un objeto. {}",
        TypeError: "Se ha producido un error de tipo. {}",
        ValueError: "Se ha producido un error de valor. {}",
        KeyError: "Se ha intentado acceder a una clave que no existe en un diccionario. {}",
        IndexError: "Se ha intentado acceder a un índice fuera del rango en una lista o tupla. {}",
        FileNotFoundError: "El archivo especificado no se ha encontrado. {}.",
        pandas.errors.ParserError: "Ocurrió un error al analizar el archivo CSV. {}.",
        pandas.errors.DtypeWarning: "Ocurrió un problema de incompatibilidad en los tipos de datos de alguna columna en el archivo CSV. {}.",
        pandas.errors.UnsupportedFunctionCall: "Ocurrió un error al llamar a una función no soportada en DataFrame de pandas. {}.",
        pandas.errors.EmptyDataError: "El DataFrame de pandas está vacío. {}.",
        #falta plotly y pio
    }
    
    @staticmethod
    def get_error_messages(exception):
        exception_message = ""
        try:
            raise exception
        except SyntaxError:
            exception_message =  "Ocurrió un error de sintaxis. {}"
        except NameError as ne:
            variable_name = ne.args[0].split("'")[1]
            exception_message =  "Se ha utilizado una variable no definida: " + variable_name + " {}"
        except AttributeError:
            exception_message =  "Se intentó realizar una operacion no soportada por un bloque. {}"
        except TypeError:
            exception_message =  "Se ha producido un error de tipo. {}"
        except ValueError as ve:
            if "fig parameter" in str(ve):
                exception_message = "Error de valor de Plotly: la entrada debe ser una Figura (bloque de Plotly)"
            else:
                exception_message =  "Se ha producido un error de valor, verifica que las entradas de los bloques sean correctas. {}"
        except KeyError:
            exception_message =  "Se ha intentado acceder a una clave que no existe en un diccionario. {}"
        except IndexError:
            exception_message =  "Se ha intentado acceder a un índice fuera del rango en una lista o tupla. {}"
        except FileNotFoundError:
            exception_message =  "El archivo especificado no se ha encontrado. {}"
        except pandas.errors.ParserError:
            exception_message =  "Ocurrió un error al analizar el archivo CSV. {}"
        except pandas.errors.DtypeWarning:
            exception_message =  "Ocurrió un problema de incompatibilidad en los tipos de datos de alguna columna en el archivo CSV. {}"
        except pandas.errors.UnsupportedFunctionCall:
            exception_message =  "Ocurrió un error al llamar a una función no soportada en DataFrame de pandas. {}"
        except pandas.errors.EmptyDataError:
            exception_message =  "El DataFrame de pandas está vacío. {}"
        except Exception:
            exception_message =  "Ocurrió un error cerca de la ejecución del código {}."

        error_info = traceback.format_exception_only(type(exception), exception)
        original_error = ''.join(error_info)
        
        error_line_number_text = get_error_line_number_text(original_error)
        personalized_error = exception_message.format(error_line_number_text).strip()
      
        return personalized_error, original_error

def get_error_line_number_text(error):
    match = re.search(r'line (\d+)', error)
    if match:
        return "\nRevisa cerca de la línea " + match.group(1)
    else: 
        return ""
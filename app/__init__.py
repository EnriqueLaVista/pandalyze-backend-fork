from flask import Flask
from .endpoints.health_check import bp as health_check_bp
from .endpoints.bd_check import bp as bd_check_bp
from .endpoints.run_python_code import bp as run_python_code_bp
from .endpoints.save_csv import bp as save_csv_bp
from .config import get_config
from .extensions import db

def create_app():

    # Creamos una instancia de la aplicación Flask
    app = Flask(__name__)

    # Configura la conexión a la base de datos, el entorno, modo debug...
    app.config.from_object(get_config())

    # Inicializa la extensión SQLAlchemy con la aplicación
    db.init_app(app)

    # Registramos los Blueprints en la aplicación
    app.register_blueprint(health_check_bp)
    app.register_blueprint(bd_check_bp)
    app.register_blueprint(run_python_code_bp)
    app.register_blueprint(save_csv_bp)
    
    return app
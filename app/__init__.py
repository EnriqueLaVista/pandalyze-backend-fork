from flask import Flask
from .routes import bp as main_bp  # Importa el Blueprint desde routes.py
from .config import get_config
from .extensions import db
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    # Creamos una instancia de la aplicación Flask
    app = Flask(__name__)

    # Configura la conexión a la base de datos, el entorno, modo debug...
    app.config.from_object(get_config())

    # Inicializa la extensión SQLAlchemy con la aplicación
    db.init_app(app)

    # Registramos el Blueprint en la aplicación
    app.register_blueprint(main_bp)

    return app
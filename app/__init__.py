from flask import Flask
from .routes import bp as main_bp  # Importa el Blueprint desde routes.py
from .config import Config
from .extensions import db


def create_app():
    # Creamos una instancia de la aplicación Flask
    app = Flask(__name__)

    # Configura la conexión a la base de datos (aquí se usa SQLite como ejemplo)
    app.config.from_object(Config())

    # Inicializa la extensión SQLAlchemy con la aplicación
    db.init_app(app)

    # Registramos el Blueprint en la aplicación
    app.register_blueprint(main_bp)

    return app
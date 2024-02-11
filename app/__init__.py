from flask import Flask
from .routes import bp as main_bp  # Importa el Blueprint desde routes.py

def create_app():
    # Creamos una instancia de la aplicación Flask
    app = Flask(__name__)

    # Registramos el Blueprint en la aplicación
    app.register_blueprint(main_bp)

    return app


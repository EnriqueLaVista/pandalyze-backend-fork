from app import create_app
from flask_cors import CORS

# Creamos la instancia de la aplicación Flask
app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)


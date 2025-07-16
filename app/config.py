import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Determina el entorno segun la variable de entorno FLASK_ENV, o defaultea a development
    env = os.getenv('FLASK_ENV', 'development')
    
    # Configuración común
    DEBUG = True if env == 'development' else False
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
    

def get_config():
    return Config()
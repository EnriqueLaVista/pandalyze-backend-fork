from app.extensions import db
from sqlalchemy import Column, Integer, String, Text

def name_to_id(name: str, h:int = 5381) -> int:
    """
    Generar ID a partir de un string utilizando DJB2.
    Retorna un número entero positivo de 32 bits.
    """
    for c in name:
        h = (h * 33) ^ ord(c)
    return h & 0xFFFFFFFF

# Define el modelo para la tabla donde se almacenará el CSV
class CSVData(db.Model):
    __tablename__ = 'csv_data'

    id = Column(Integer, primary_key=True, autoincrement=False)  
    filename = Column(String(100), nullable=False, unique=True)
    data = Column(Text, nullable=False)

    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        self.id = name_to_id(filename)

    def __repr__(self):
        return '<CSV %r>' % self.filename

    @classmethod
    def get_csv_by_id(cls, csv_id):
        return cls.query.get(csv_id)

    @classmethod
    def get_csv_by_filename(cls, filename):
        return cls.query.filter_by(filename=filename).first()

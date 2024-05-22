from app.extensions import db
from sqlalchemy import Column, Integer, String, Text

# Define el modelo para la tabla donde se almacenará el CSV
class CSVData(db.Model):
    __tablename__ = 'csv_data'

    id = Column(Integer, primary_key=True)
    filename = Column(String(100), nullable=False)
    data = Column(Text, nullable=False)

    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def __repr__(self):
        return '<CSV %r>' % self.filename
    
    @classmethod
    def get_csv_by_id(cls, csv_id):
        return cls.query.get(csv_id)

    @classmethod
    def get_csv_by_filename(cls, filename):
        return cls.query.filter_by(filename=filename).first()
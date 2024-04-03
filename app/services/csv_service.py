import pandas as pd
from io import StringIO

def save_csv_data(filename, data):
    from ..models.csv_model import CSVData
    from .. import db
    
    # Almacena la información del CSV en la base de datos
    csv_data = CSVData(filename=filename, data=data)
    db.session.add(csv_data)
    db.session.commit()

    return csv_data.id

def read_csv(csv_id): 
    from app.models.csv_model import CSVData
    csvData = CSVData.get_csv_by_id(csv_id)
    df = pd.read_csv(StringIO(csvData.data))
    
    return df

import pandas as pd
from io import StringIO
from app.models.csv_model import CSVData
from app.extensions import db

# Almacena la información del CSV en la base de datos
def save_csv_data(filename, data):
    csv_data = CSVData(filename=filename, data=data)
    db.session.add(csv_data)
    db.session.commit()

    return csv_data.id, get_csv_columns_names(data)

def read_csv(csv_id): 
    csvData = CSVData.get_csv_by_id(csv_id)
    df = pd.read_csv(StringIO(csvData.data))
    
    return df

def get_csv_by_content(csv_content):
    csv = CSVData.query.filter_by(data=csv_content).first()
    if csv:
        return csv.id, get_csv_columns_names(csv.data)
    else:
        return None, None


def get_csv_columns_names(data):
    return list(pd.read_csv(StringIO(data)).columns)
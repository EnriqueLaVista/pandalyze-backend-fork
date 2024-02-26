def save_csv_data(filename, data):
    from ..models.csv_model import CSVData
    from .. import db
    
    # Almacena la información del CSV en la base de datos
    csv_data = CSVData(filename=filename, data=data)
    db.session.add(csv_data)
    db.session.commit()

from flask import Blueprint, jsonify
from app.models.csv_model import CSVData
from app import db

bp = Blueprint('bd_check', __name__)

@bp.route('/bdCheck')
def bd_check():
    try:
        count = CSVData.query.count()
        return jsonify({'message': 'OK!', 'count': count}), 200
    except Exception as e:
        db.create_all()
        CSVData.query.all()
        return jsonify({'message': e}), 200